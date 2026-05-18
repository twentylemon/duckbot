# Add Satisfactory 1.2 Recipe Parts Cost Multiplier to `/satisfy`

## Context

Satisfactory 1.2 (March 2026) introduced a Game Modes menu with four dials:

| Dial | Range | Solver-relevant? |
|---|---|---|
| Recipe Parts Cost Multiplier | 0.25x – 2x | **Yes** — scales recipe inputs |
| Space Elevator Cost Multiplier | 0.25x – 100x | No — affects target rates only, user can set targets manually |
| Power Consumption Multiplier | 0.25x – 5x | No — solver has no factory-wide power constraint to scale |
| Resource Node Randomization / Purity | enum | No (out of scope per user) |

Per your answer, scope is **Recipe Parts Cost Multiplier only**. This dial changes how many input parts every non-Space-Elevator recipe needs to craft, leaving output rates unchanged. On 0.5x a Reinforced Iron Plate recipe would take 15 IronPlate + 30 Screw instead of 30 + 60 per craft cycle; the solver's `recipe.inputs * use` term must reflect that or solutions will be wrong for non-default worlds.

The in-game dial offers eight presets: **0.25, 0.50, 0.75, 1, 1.25, 1.50, 1.75, 2** (from the official patch notes).

The current solver models recipe inputs in exactly one place (`solver.py:88`), so the change is small and localized.

### Dropping recipes that can't physically run

When `multiplier > 1`, a recipe's per-minute input rate scales up. If that scaled rate exceeds the belt (1200/min solid) or pipe (600/min fluid) limit defined in `item.py:transport_limit`, a single machine literally cannot be fed and the recipe is unusable in-game. We drop those `ModifiedRecipe` variants from the solver's recipe set rather than letting the LP propose physically impossible solutions.

This mirrors the existing `ModifiedRecipe.capped_shard_scale` logic (recipe.py:50–53), which already caps overclock so neither inputs nor outputs blow past transport limits. Adding a multiplier-aware filter on top of that is consistent.

(For `multiplier ≤ 1`, scaled rates stay at or below the original ≤ transport_limit, so no recipe gets dropped.)

## Approach

Store the multiplier as a per-user factory field, apply it in the cost-computation in the solver, and add a slash command + state display for it. Do **not** push it into `ModifiedRecipe` itself — the multiplier is a property of the world the user is playing in, not of the recipe.

### 1. `duckbot/cogs/games/satisfy/factory.py` — add field

Add `parts_cost_multiplier: float = 1.0` to the `Factory` dataclass alongside `power_shards` and `sloops`.

### 2. `duckbot/cogs/games/satisfy/solver.py` — apply multiplier and filter

a) In `amount_by_item_expressions`, change the `cost` closure (line 87–90) so input rates are scaled:

```python
def cost(recipe: ModifiedRecipe, use: Var | LinExpr):
    costs = dict((item, -use * rate * factory.parts_cost_multiplier) for item, rate in recipe.inputs.items())
    income = dict((item, use * rate) for item, rate in recipe.outputs.items())
    return costs, income
```

This is the only place in the solver that reads `recipe.inputs` for the LP — `regular_limit` only inspects raw recipes (whose inputs are empty) and `generate_raw` only uses outputs.

b) Add a transport-feasibility filter and apply it inside `optimize` before building the LP, alongside the existing `limit_recipes` call:

```python
from .item import transport_limit  # already imported indirectly; add to existing imports

def transport_feasible(recipe: ModifiedRecipe, multiplier: float) -> bool:
    return all(rate * multiplier <= transport_limit(item) for item, rate in recipe.inputs.items())
```

And in `optimize`, change:

```python
recipes = limit_recipes(factory.recipes, factory.power_shards, factory.sloops)
```

to:

```python
recipes = [r for r in limit_recipes(factory.recipes, factory.power_shards, factory.sloops)
           if transport_feasible(r, factory.parts_cost_multiplier)]
```

(Filtering belongs in the solver, not the cog, so the rule is enforced even if `factory.recipes` is populated by some future code path.)

**Caveat (acceptable):** `ModifiedRecipe.capped_shard_scale` (recipe.py:50) caps overclock against the *unscaled* input rate. With a reduced parts cost the belt would actually saturate later, so machines could theoretically overclock further than `capped_shard_scale` allows. The solver will be conservative in that edge case but never wrong. Threading the multiplier into `ModifiedRecipe` would require restructuring how `as_slooped` is called from `satisfy.py:142–144`; not worth it for a corner case.

### 3. `duckbot/cogs/games/satisfy/satisfy.py` — add slash command

Add a command after `add_booster`:

```python
@satisfy.command(name="parts-cost", description="Set the recipe parts cost multiplier (Satisfactory 1.2 game mode). Default 1.0.")
async def set_parts_cost(self, context: Context, multiplier: float):
    if multiplier < 0:
        raise ValueError("Parts cost multiplier must be non-negative.")
    factory = self.factory(context)
    factory.parts_cost_multiplier = multiplier
    self.save(context, factory)
    await context.send(embed=factory_embed(factory), delete_after=60)
```

Validate non-negative only — solving with the game's max (2x) is supported, but so is throwing the 100x Space-Elevator dial at the parts cost just to see what happens. Register it in the `@*.error` chain at the bottom of the class (line 190–201).

Add an autocomplete for the `multiplier` parameter that surfaces the values the in-game dial actually offers (0.25, 0.5, 1.0, 2.0). The user can still type any positive number; autocomplete is convenience only. Follow the autocomplete pattern at satisfy.py:162–164 (boost_items):

```python
@set_parts_cost.autocomplete("multiplier")
async def parts_cost_multipliers(self, interaction: Interaction, current: str) -> List[Choice[float]]:
    return [Choice(name=f"{v}x", value=v) for v in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]]
```

### 4. `duckbot/cogs/games/satisfy/pretty.py` — show in embed

In `factory_embed`, surface the multiplier only when it differs from 1.0 — keeps the embed unchanged for default-game users. Easiest spot: append to the `Inputs` field (alongside `power_shards`/`sloops` blocks), e.g. `f"{factory.parts_cost_multiplier}x **Parts Cost**"` when `factory.parts_cost_multiplier != 1.0`.

### 5. Tests

- `tests/cogs/games/satisfy/satisfy_test.py` — add a test for `set_parts_cost`: sets the field (including a value above the game's 2x max, e.g. 5.0, to confirm we don't gate it), sends the embed, rejects negative values. Follow the pattern at lines 58–72 (toggle_maximize).
- `tests/cogs/games/satisfy/solver_test.py` — add two cases mirroring existing tests in that file:
  1. `parts_cost_multiplier = 0.5` with a simple chain (e.g. IronOre → IronIngot → IronPlate): consumed IronOre is halved.
  2. `parts_cost_multiplier = 2.0` for a recipe whose scaled input would exceed `transport_limit`: that recipe is dropped from the solution (use a high-throughput recipe whose input is already near 1200/min so 2x clearly exceeds it).

No new test file needed. No changes to `recipe.py`, `weights.py`, `recipe_banks.py`, `graph.py`, or `building.py`.

## Files modified

- `duckbot/cogs/games/satisfy/factory.py` — add `parts_cost_multiplier` field
- `duckbot/cogs/games/satisfy/solver.py` — apply multiplier in cost closure (1 line)
- `duckbot/cogs/games/satisfy/satisfy.py` — add `/satisfy parts-cost` command + error hook
- `duckbot/cogs/games/satisfy/pretty.py` — conditionally render in Inputs field
- `tests/cogs/games/satisfy/satisfy_test.py` — command test
- `tests/cogs/games/satisfy/solver_test.py` — multiplier-effect test

## Verification

1. `pytest tests/cogs/games/satisfy/` — confirm new + existing tests pass.
2. `pytest` — full suite (includes lint/format).
3. Boot the bot (`python -m duckbot` with `DISCORD_TOKEN` set) and walk through in Discord:
   - `/satisfy reset`
   - `/satisfy parts-cost 0.5`
   - `/satisfy state` — embed shows `0.5x Parts Cost`
   - `/satisfy output IronPlate 20`
   - `/satisfy solve` — solution should consume ~15 IronOre/min (half of the 30 IronOre/min default)
   - `/satisfy parts-cost 1.0` then re-solve — back to ~30 IronOre/min
   - `/satisfy parts-cost 2.0` then re-solve — any recipe whose scaled input would exceed the belt/pipe limit is absent from the solution
   - `/satisfy parts-cost 100` — accepted; many recipes will be filtered out as infeasible but the solver still runs on what remains
   - `/satisfy parts-cost -1` — rejected with the non-negative validation error
   - In Discord's slash-command UI, `/satisfy parts-cost ` shows the eight in-game presets (0.25x through 2.0x in 0.25 steps)
