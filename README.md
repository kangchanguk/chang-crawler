# shopping mall crawler(쇼핑몰 크롤러)   



### Installation

Install the dependencies and devDependencies and start the server.

```sh
$ pip install -r chang-crawler.txt
```
and
please install chromedriver for your chrome version
[chromedriver 다운로드]("https://chromedriver.chromium.org/downloads")

반드시 같은 new-crawler.py 파일과 같은 폴더에 chromedriver가 있어야 합니다.
For production environments...

```sh
$ python
$ maria DB
```

## INTRODUCE

먼저 csv파일에 쇼핑몰 이름과 쇼핑몰 주소를 입력해주세요 csv파일에 적힌 쇼핑몰들의 이미지들을 긁어옵니다.
현재 제공되는 쇼핑몰 크롤러는 메인 페이지 이미지와 해당 이미지와 링크된 페이지의 이미지들을 긁어오고 링크된 페이지의 여러개의 이미지가 
합쳐져 있는 통 이미지의 경우 잘라서 각각 저장해줍니다.

![슬라이드2](https://user-images.githubusercontent.com/26477881/73994465-f4415380-4998-11ea-941c-a36d0feb6dcc.JPG)

![슬라이드3](https://user-images.githubusercontent.com/26477881/73994468-f7d4da80-4998-11ea-85d0-e54616147164.JPG)


![슬라이드4](https://user-images.githubusercontent.com/26477881/73994474-f99e9e00-4998-11ea-98bf-b4a82c2136bc.JPG)  

![슬라이드5](https://user-images.githubusercontent.com/26477881/73994476-fb686180-4998-11ea-9baf-42e11fd6feca.JPG)

![슬라이드6](https://user-images.githubusercontent.com/26477881/73994480-fd322500-4998-11ea-8df9-5ce3202e6091.JPG)


#### License
----

kang chang uk(강창욱)


**Free Software, HellO everyone!**





