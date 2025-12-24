import os
import modpack
import secrets

from flask import make_response, render_template, send_from_directory, Flask, request, redirect

filepath = "modlist.md"

infos,categories = modpack.read_modlist(filepath)
mods_slugs = sum([c["mods"] for c in categories], [])

app = Flask("test")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config')
def selection_page():
    mods = modpack.get_modrinth_infos(mods_slugs, infos["mc_version"])
    return render_template(
        'client.html',
        categories=categories, 
        mods=mods,
    )

@app.post("/pw")
def packwiz_generate():
    # création du dossier
    token = secrets.token_urlsafe(6)
    path = os.path.join("instances", token)
    os.makedirs(path, exist_ok=True)

    mp = modpack.ModPack(path, **infos)
    mp.add_mods(request.form)
    
    return redirect(f"/pw/{token}/pack.toml", 303)

@app.route('/pw/<path:path>')
def packwiz_raw(path):
    r = make_response(send_from_directory("instances", path))
    r.mimetype = "text/plain"
    return r