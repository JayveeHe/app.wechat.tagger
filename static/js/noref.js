/**
 * Created by jayvee on 15/12/18.
 */
function noref() {
    //$.browser.webkit ||
    $.event.add(window, "load", function () { //webkit系列浏览器啥也不做
        //把所有带有rel=noreferrer的链接找出来变量处理
        $("a[href][rel~=noreferrer], area[href][rel~=noreferrer]").each(function () {
            var b, e, c, g, d, f, h;
            b = this;    //b表示当前链接dom对象
            c = b.href;  //保存原始链接
            $.browser.opera ? (b.href = "http://www.google.com/url?q=" + encodeURIComponent(c), b.title || (b.title = "Go to " + c)) : (d = !1, g = function () { //Opera做了些啥暂不管
                b.href = "javascript:void(0)"
            }, f = function () {
                b.href = c
            }, $(b).bind("mouseout mouseover focus blur", f).mousedown(function (a) { //鼠标out over focus blue都把链接还原
                a.which === 2 && (d = !0) //鼠标down时，且鼠标中间按下时，把标志d设成true
            }).blur(function () { //blur把标志d设成false
                d = !1
            }).mouseup(function (a) {
                if (!(a.which === 2 && d)) return !0;
                g();
                d = !1;
                setTimeout(function () {
                    alert("Middle clicking on this link is disabled to keep the browser from sending a referrer.");
                    f()
                }, 500);
                return !1
            }), e = "<html><head><meta http-equiv='Refresh' content='0; URL=" + $("<p/>").text(c).html() + "' /></head><body><    /body></html>", $.browser.msie ? $(b).click(function () { //e是一个0秒自动刷新的页面，指向原始链接，但是没搞懂为什么搞个p标签在这里？？
                var a;                             //如果是IE的话
                switch (a = this.target || "_self") {
                    case "_self":
                    case window.name:
                        a = window;
                        break;
                    default:                           //如果原始链接的目标是本窗口，则在本窗口操作
                        a = window.open(null, a)       //如果原始链接的目标不是本窗口，则用js open一个空窗口
                }
                a = a.document;
                a.clear();                         //清除窗口的document
                a.write(e);                        //写入上面构造的0秒自动刷新的页面
                a.close();                         //关闭文档使其展示出来
                return !1                          //如果非IE(firefox), 是用的'Data URI scheme'承载0秒自动刷新的页面
            }) : (h = "data:text/html;charset=utf-8," + encodeURIComponent(e), $(b).click(function () { //最后js触发点击
                this.href = h;
                return !0
            })))
        })
    })
}