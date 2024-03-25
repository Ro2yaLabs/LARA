# LARA

### Installation Guide

1. Clone the repo
```shell
git clone https://github.com/Mahmoud-ghareeb/LARA.git
``` 

1. Create Python Environment
```shell
conda create --name lara python==3.12.2
```

2. Activate the environment
```shell
conda activate lara
```

3. install the requirments
```shell
pip install -r requirements.txt
```

4. Rename .env.example to .env and add the secret keys of 
    - openai
    - elevenlabs


5. Run the following docker command

```shell
#CHANGE M:\Projects\ro2ya\LARA\store => to the location in your hard disk
docker run -p 8000:8000 -e CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER="chromadb.auth.token.TokenConfigServerAuthCredentialsProvider" -e CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.token.TokenAuthServerProvider" -e CHROMA_SERVER_AUTH_CREDENTIALS="zed@12345678" -e CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER="X_CHROMA_TOKEN" -v M:\Projects\ro2ya\LARA\store:/chroma/chroma -d chromadb/chroma
```

6. Download mpv for streaming and put it in program files
```shell
https://sourceforge.net/projects/mpv-player-windows/
```

7. Start the app
```shell
uvicorn main:app --port 8080
```

8. APIs documentation at 
``` shell
https://example.com
```

9. You can test the app from test_main.pynb script


