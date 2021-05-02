FROM python:3.8
# RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list && \
#     apt-get update && apt-get -y install --no-install-recommends \
#     ffmpeg \
#     fortune-mod fortunes fortunes-off cowsay cowsay-off \
#     firefox \
#   && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install --no-install-recommends \
    ffmpeg \
    fortune-mod fortunes fortunes-off cowsay cowsay-off \
    firefox-esr \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH "$PATH:/usr/games"
RUN python -m pip install --upgrade pip
WORKDIR /duckbot
COPY requirements.txt .
RUN python -m pip install -r ./requirements.txt
COPY resources/ ./resources
COPY duckbot/ ./duckbot
ENV DUCKBOT_ARGS ""
ENTRYPOINT [ "python" ]
CMD [ "-u", "-m", "duckbot" ]
