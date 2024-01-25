import fastapi
from fastapi.responses import HTMLResponse


app = fastapi.FastAPI()



@app.get("/")
async def home():
    html_content = """
    <html>
        <head>
            <title>Welcome</title>
             <style>
                body {
                    text-align: center;
                    margin: 20px;
                }
                h1 {
                    margin: 5px 0;
                    font-family: "Book Antiqua", Palatino, serif;
                    font-size: 48px;
                }
                h2 {
                    margin: 5px 0;
                    font-family: "Book Antiqua", Palatino, serif;
                    font-size: 64px;
                }
                p {
                    margin: 65px;
                }
                .input-container {
                    width: 300px;
                    margin: 30px auto;
                    text-align: left;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                }
                input {
                    width: 100%;
                    padding: 10px;
                    box-sizing: border-box;
                }
                button {
                    color: black;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to</h1>
            <h2>Collaborate</h2>
            <p> </p>

            <div class="input-container">
                <label>Name:</label>
                <input type="text" placeholder="Input name">
            </div>

            <div class="input-container">
                <label>Password:</label>
                <input type="text" placeholder="Input password">
            </div>

             <a href="/home">
                <button>Login</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/home")
async def home():
    html_content = """
    <html>
        <head>
            <title>Test</title>
            <style>
                body {
                    text-align: center;
                    margin: 20px;
                }
                h1 {
                    margin: 5px 0;
                    font-family: "Book Antiqua", Palatino, serif;
                    font-size: 65px;
                }
                .button-container button {
                    margin: 100 100px;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <h1>Collaborate</h1>
            <div class="button-container">
                <button type="button">Eddit existing document</button>
                <button type="button">Create new document</button>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)