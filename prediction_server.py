#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import keras, io, base64
from PIL import Image
import numpy as np

model_file = 'fruits.hdf5'
port = 8180
target_width = 224
target_height = 224
target_classes = ['bad', 'good']


model = keras.models.load_model(model_file)

class BaseHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        s = '''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
  </head>
  <body>
    <h3>Image Check</h3>
    <form>
      <label>Image File: <input id="file" type="file" accept="image/*"/></label>
    </form>
    <p id="prediction"></p>
    <img id="img" src="" width="50%"/>
    <script>
      $("#file").change(function(){
        var reader = new FileReader();
        $("#prediction").html("");
        console.log(this.files[0].name);
        var filename = this.files[0].name;
        reader.onload = function() {
          $("#img").attr("src", reader.result);
          $.ajax({url:"/", type:"POST", data:filename + "," + reader.result})
          .done((res)=>$("#prediction").html(res))
          .fail((res)=>console.error(res));
        }
        reader.readAsDataURL(this.files[0]);
      });
    </script>
  </body>
</html>
        '''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(s, 'utf-8'))
        # print(s)

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        content = self.rfile.read(content_len).decode('UTF-8')
        contents = content.split(',', 1)
        filename = contents[0]
        content = contents[1].replace('data:image/jpeg;base64,', '')
        image = np.array(Image.open(io.BytesIO(base64.b64decode(content)))
                         .resize((target_width, target_height))).transpose(1, 0, 2)
        image = np.expand_dims(image, axis=0)
        result = model.predict(image)
        # print(str(result))
        answer = target_classes[result[0].argmax()]
        print(filename + ':' + answer)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-length', len(answer))
        self.end_headers()
        self.wfile.write(bytes(answer, 'utf-8'))

baseHttpServer = HTTPServer(('', port), BaseHttpServer)
try:
    baseHttpServer.serve_forever()
except KeyboardInterrupt:
    pass

baseHttpServer.server_close()
