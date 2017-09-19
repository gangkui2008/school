# school

## Overview ##
A spider using scrapy to crawl Wuhan primary schools info from http://esf.wuhan.fang.com/school/.

And

A shell script to filter out the good schools.

## Prerequisite ##
Python

[scrapy](https://github.com/scrapy/scrapy)

[unicodecsv](https://github.com/jdunck/python-unicodecsv)

## Usage ##
Clone this repo.

Start the crawl:

```
cd school
scrapy crawl school
```

A csv file named _武汉学校{$date}.csv_ will be generated in the school/output/ folder when the crawl finished.

Then you can filter out the good schools from the csv file with the providing shell script:

```
cd output
./getGoodSchool.sh 武汉学校20170830.csv
```

The good school list will be stored in school/output/goodSchool.csv.
