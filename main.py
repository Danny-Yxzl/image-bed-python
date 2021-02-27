# coding:utf-8
import os
import random

from flask import *


app = Flask(__name__)
app.secret_key = "yxzlimagecdn"
this_dir = os.path.dirname(__file__)


def generate_random_str(random_length=16):
    random_str = ""
    for i in range(random_length):
        random_str += random.choice("ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789")
    return random_str


@app.route("/vip", methods=["GET", "POST"])
def vip():
    if request.method == "POST":
        f = request.files["file"]
        if len(f.read()) == 0:
            return redirect("/")
        f.seek(0)
        if session.get("name"):
            filename = "%s/%s" % (session.get("name"), f.filename)
            if not os.path.isdir("%s/static/%s" % (this_dir, session.get("name"))):
                os.makedirs("%s/static/%s" % (this_dir, session.get("name")))
        else:
            return render_template("vip.html", username=request.args.get("name"), message="错误：请指定用户名！")
        upload_path = "%s/static/%s" % (this_dir, filename)
        f.save(upload_path)
        f.close()
        return render_template("show.html", img_url="static/%s" % filename)
    else:
        session["name"] = request.args.get("name") \
            if request.args.get("name") and request.args.get("name") != "free" \
            else session.get("name")
        return render_template("vip.html", username=session.get("name"))


@app.route("/", methods=["GET", "POST"])
def free():
    # 8388608
    if request.method == "POST":
        f = request.files["file"]
        if len(f.read()) == 0:
            return redirect("/")
        elif len(f.read()) > 8388608:
            return render_template("index.html", message="上传失败：免费用户最大上传限制为8MB！")
        f.seek(0)
        filename = "%s.%s" % (generate_random_str(), f.filename.split(".")[-1])
        upload_path = "%s/static/free/%s" % (this_dir, filename)
        f.save(upload_path)
        f.close()
        return render_template("show.html", img_url="static/free/%s" % filename)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
