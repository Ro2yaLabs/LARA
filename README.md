# LARA

### Installation Guide

1. Clone the repo
- `git clone https://github.com/Mahmoud-ghareeb/LARA.git`   

1. Create Python Environment
- `conda create lara python==3.12.2`

2. Activate the environment
- `conda activate lara`

3. install the requirments
- `pip install -r requirements.txt`

4. Run the following docker command
BUT CHANGE M:\Projects\ro2ya\LARA\store => to the location in your hard
- ```docker run -p 8000:8000 -e CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER="chromadb.auth.token.TokenConfigServerAuthCredentialsProvider" -e CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.token.TokenAuthServerProvider" -e CHROMA_SERVER_AUTH_CREDENTIALS="zed@12345678" -e CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER="X_CHROMA_TOKEN" -v M:\Projects\ro2ya\LARA\store:/chroma/chroma -d chromadb/chroma```

5. Download mpv for streaming and put it in program files 
- `https://sourceforge.net/projects/mpv-player-windows/`

5. Start the app
- `uvicorn main:app --port 8080`

6. test the app from test_main.pynb script


