# i211 Flask Template

Template repository for building a flask website.

## Quickstart

**MacOS / Linux / ChromeOS**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows + PowerShell**

<details>
<summary>Do you see a red permissions error when activating the environment?</summary>

You might need to set the execution policy on your machine. This should only need to be done once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

Check your `flask` installation:

```bash
python -m flask --version
```

<details>
<summary>Did you see an error like <code>ImportError: cannot import name 'Mapping' from 'collections'</code>?</summary>

Run the patch script:

```powershell
python patch_jinja.py
```

</details>

## Primary Sources

| page | url | summary |
| :--- | :---- | :----- |
| Bootstrap 5.3 | https://getbootstrap.com/docs/5.3/getting-started/introduction/ | "Bootstrap is a powerful, feature-packed frontend toolkit." |
| Jinja 2.10.x | https://jinja.palletsprojects.com/en/2.10.x/ | Jinja is a templating language for Python. |
| `templates/base.html` | https://getbootstrap.com/docs/5.3/examples/sticky-footer-navbar/ | The `base.html` here is based off the Bootstrap 5.3 "*Sticky footer with fixed navbar*" template. |
| Luddy CGI Server | https://uisapp2.iu.edu/confluence-prd/pages/viewpage.action?pageId=130122153 | The Luddy cgi server allows the running of arbitrary programs (e.g. perl, python, scheme, bash, etc). |

## Common Operations

Logging into `silo`:

```bash
ssh username@silo.luddy.indiana.edu
```

Debugging cgi errors:

```bash
ssh username@silo.luddy.indiana.edu
ssh username@cgi.luddy.indiana.edu
less +F /var/log/apache2/error.log
```

Logging into MariaDB (replace USER/PASSWORD/DATABASE):

```bash
mysql -h db.luddy.indiana.edu -u USER --password=PASSWORD -D DATABASE
```

## Other Notes

**Q**: *How do I know what packages are installed on the server?*

**A**: Here's a one-liner:

```bash
pip freeze | grep "click\|Flask\|itsdangerous\|Jinja2\|MarkupSafe\|Werkzeug\|PyMySQL"
```
