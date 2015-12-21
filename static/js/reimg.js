/**
 * Created by jayvee on 15/12/18.
 */
function changeData(data, tag) {
    for (var i = 0; i < data.length; i++) {
        if (!data[i].hasAttribute("data-src") && data[i].hasAttribute("src") && (data[i].getAttribute("src")).lastIndexOf('http://', 0) === 0 && (data[i].getAttribute("src")).indexOf('chuansong.me/') == -1) {
            data[i].setAttribute("data-src", data[i].getAttribute("src"));
        }
        if (data[i].hasAttribute("data-src")) {
            datasrc = data[i].getAttribute("data-src");
            datasrc = datasrc.replace("https://v.qq.com/", 'http://v.qq.com/');
            data[i].setAttribute("src", (tag == 'image' && datasrc.indexOf('http://read.html5.qq.com/image') == -1) ? "http://read.html5.qq.com/image?imageUrl=" + datasrc : datasrc);
            data[i].removeAttribute("data-src");
        }
    }
}

//function startChange() {
//    console.log("start change")
//
//    console.log(imgs)
//    changeData(imgs, 'image');
//    changeData(videos, 'video');
//}


//function addiframe(data, tag) {
//    for (var i = 0; i < data.length; i++) {
//        if (!data[i].hasAttribute("data-src") && data[i].hasAttribute("src") && (data[i].getAttribute("src")).lastIndexOf('http://', 0) === 0 && (data[i].getAttribute("src")).indexOf('chuansong.me/') == -1) {
//            data[i].setAttribute("data-src", data[i].getAttribute("src"));
//        }
//        if (data[i].hasAttribute("data-src")) {
//            datasrc = data[i].getAttribute("data-src");
//            datasrc = datasrc.replace("https://v.qq.com/", 'http://v.qq.com/')
//            data[i].setAttribute("src", (tag == 'image' && datasrc.indexOf('http://read.html5.qq.com/image') == -1) ? "http://read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=" + datasrc : datasrc);
//            data[i].removeAttribute("data-src");
//        }
//    }
//}