<div align="center">
<h1>aniinfo</h1>
<p>the best cli tool for searching up info on anime and manga series<p>
</div>

![searching up anime](https://i.imgur.com/b58BIUh.gif)   

## installation  

install from `pypi`:

```bash
pip install aniinfo
```
or from `git`:

```bash
pip install git+https://github.com/sleepntsheep/aniinfo/
```

## usage

```
aniinfo -a [anime-name] --page [page-num]  
aniinfo -m [manga-name] --page [page-num]  
aniinfo -c [characters-name] --page [page-num]  
```

## example config

```
{
	"title_language"     : "romaji", 
	"comment_1"          : "title_language can be romaji, english , or native",

	"anime_show_studio"  : true,
	"anime_show_season"  : true,
	"anime_show_genres"  : false,
	"anime_show_status"  : true,
	"anime_show_episode" : true,
	"anime_show_format" : true,

	"manga_show_status"  : true,
	"manga_show_genres"  : true,
	"manga_show_chapter" : true,
	"manga_show_volume"  : true,

	"char_show_birthdate": true,
	"char_show_gender"   : true,
	"char_show_age"      : true,
	"char_name_format"   : "full",
	"comment_2"          : "char_name_format can be first, last, full, or native",

	"per_page"           : 10
}
```

in `~/.config/aniinfo/config.json`
