from django.http import HttpResponse

def home(request):
    html = """
    <html>
        <head>
            <title>BorderHearts Kennel</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    font-family: Arial, sans-serif;

                    /* --- TŁO STRONY --- */
                    background-image: url('/static/kennel/border.jpg');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                }

                .box {
                    background: rgba(255, 255, 255, 0.75);
                    padding: 40px 60px;
                    border-radius: 14px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
                    font-size: 32px;
                }
            </style>
        </head>
        <body>
            <div class="box">
                Hello from Border Collie Kennel 🐶<br>
                <strong>— BorderHeart —</strong><br>
                Works!
            </div>
        </body>
    </html>
    """
    return HttpResponse(html)
