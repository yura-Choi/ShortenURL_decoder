import requests
from urllib.parse import urlparse
import time

class Decode:
    def __init__(self, input_path, output_path):
        self.input_file = open(input_path, mode='r', encoding='utf-8')
        self.output_file = open(output_path, mode='a', encoding='utf-8')
        self.urls = []
        
        url = self.input_file.readline()
        while url:
            url = url.rstrip()
            if not urlparse(url).scheme:
                url = "https://" + url

            self.urls.append(url)
            url = self.input_file.readline()

    def decode(self):
        for url in self.urls:
            self.print_result(url)

            try:
                response = requests.get(url)
            except:
                message = "  invalid url or timeout\n"
                self.print_result(message)
                continue

            i = 1
            for res in response.history:
                if res.status_code // 100 == 3 and res.headers['Location']:
                    message = ""
                    for j in range(i-1):
                        message += "  "
                        print("  ", end='')
                    message += "[" + str(i) + "] " + res.headers['Location']
                    self.print_result(message)
                i += 1
            self.print_result("")
                    
            time.sleep(2)
        
        self.close()
    
    def print_result(self, message):
        print(message)
        self.output_file.write(message+"\n")
    
    def close(self):
        self.input_file.close()
        self.output_file.close()

if __name__ == "__main__":
    input_path = input("> input file path to decode: ")
    output_path = input("> input file path to save: ")

    Decode(input_path, output_path).decode()
