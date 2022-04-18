# Moodle peer-review assignment bulk file downloader

## Basic Usage

Download all files:

```python
python moodle_assignmet_dl.py

```

Continue a pariton download:

```python
python moodle_assignmet_dl.py number
```

where `number` is the next assignment which is not yet downloaded, so for
example, if the first 10 files (000-009) are downloaded already, use

```python
python moodle_assignmet_dl.py 10
```

to download 010- onwards

## Requirements

- python >= 3.10
- BeautifulSoup

## Settings

Inside `settings.py` you need to set the following:

- `COOKIES` is a dict, containing the `"MoodleSession"` key, with it's value
  being your cookie for your particular session; obtain it by copying it from
  your browser's developer tools.
  - for example: `{"MoodleSession": "tush1fr8nfm0ao7r2vc9k5k8mu"}`
- `DL_PAGE_ADDR` is a string containing the url for the moodle peer-review tool;
  it works best if you set to see all entries in the moodle web interface,
  so the sript actually sees all the links at once, as it will not step
  through the pages for you
  - for example: `"https://moodle2.inf.u-szeged.hu/moodle38/mod/workshop/view.php?id=83"`
- `DL_DIR` is a string containing a preferably absolute path to the (already
  existing) directory, to where the files will be downloaded
  - for example `"/home/example/Downloads/bulk_moodle/"`
- `DEFAULT_FILE_EXT` is a string containing the file extenison that all files
  will have, use the correct one for the files you'll be receiving
  - for example `"zip"`

## Notes

If for some reason the moodle server does not respond, the script automatically
times out, and retries to download in 5 second increments

Once the download links are scraped, the script will cache them into `link_cache.json`,
so in the event you stop and retry running the script, it wil skip this step, and
and use the cached addresses, as long as the source address in the cache matches
the address you're trying to download from, if not, the script will retrieve the
links again, and overwrite the exisitng cache.
