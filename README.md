# System Info


## Requirements
- Telegram bot token
- Telegram Client Id

## Commands
- ```/info```
- ```/cpu```
- ```/disk```
- ```/memory```
- ```/temperatur```

## Setup

- Build the docker image
    ```
    docker build -t snow/system-info:latest . 
    ```
- Run docker image

    ```
    docker run -d \
        -e botToken="<bot Token>" \
        -e chatId="<Telegram client Id>" \
        snow/system-info
    ```    
- Start containers automatically on start up
    ```
    docker run -d --restart unless-stopped\
        -e botToken="<bot Token>" \
        -e chatId="<Telegram client Id>" \
        snow/system-info
    ```    
    

Parameter | Function
------------ | -------------
`-e botToken` | set up a bot [Bot Father](https://t.me/botfather)
`-e chatId` |  Get your chat ID form [Id Bot](https://telegram.me/myidbot)
