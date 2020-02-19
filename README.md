# shopping mall crawler(쇼핑몰 크롤러)   



### Installation

Install the dependencies and devDependencies and start the server.

```sh
$ pip install -r chang-crawler.txt
```
and
please install chromedriver for your chrome version
[chromedriver 다운로드]("https://chromedriver.chromium.org/downloads")

반드시 같은 newcrawler.py 파일과 같은 폴더에 chromedriver가 있어야 합니다.
For production environments...

```sh
$ python
$ maria DB
```

## INTRODUCE

먼저 csv파일에 쇼핑몰 이름과 쇼핑몰 주소를 입력해주세요 csv파일에 적힌 쇼핑몰들의 이미지들을 긁어옵니다.
현재 제공되는 쇼핑몰 크롤러는 메인 페이지 이미지와 해당 이미지와 링크된 페이지의 이미지들을 긁어오고 링크된 페이지의 여러개의 이미지가 
합쳐져 있는 통 이미지의 경우 잘라서 각각 저장해줍니다.

![슬라이드2](https://user-images.githubusercontent.com/26477881/74807477-eb069e00-532b-11ea-803f-b6eff054c7aa.JPG)

![슬라이드3](https://user-images.githubusercontent.com/26477881/74807539-0ffb1100-532c-11ea-98c6-f0b6455245c8.JPG)

![슬라이드4](https://user-images.githubusercontent.com/26477881/74807570-22754a80-532c-11ea-9fee-5e4d3d0b7a7e.JPG)

![슬라이드5](https://user-images.githubusercontent.com/26477881/74807598-302ad000-532c-11ea-9b99-b42a1cc554d8.JPG)

![슬라이드6](https://user-images.githubusercontent.com/26477881/74807618-3a4cce80-532c-11ea-8f10-dad90445015d.JPG)



#### License
----

**LOOKO**







