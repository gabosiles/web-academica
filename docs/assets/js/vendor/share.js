(function (o, r) { // Función autoejecutable que recibe 'window' y 'document' como argumentos
    "use strict";

    // Constructor de la clase Sharer
    var i = function (t) {
        this.elem = t; // Guarda el elemento HTML que disparó el evento
    };

    // Método estático: inicializa todos los elementos con [data-sharer]
    i.init = function () {
        var t = r.querySelectorAll("[data-sharer]"), // Busca todos los elementos con data-sharer
            e, 
            a = t.length;
        for (e = 0; e < a; e++) {
            // Añade evento click para llamar a i.add()
            t[e].addEventListener("click", i.add);
        }
    };

    // Método estático: función manejadora del click
    i.add = function (t) {
        var e = t.currentTarget || t.srcElement; // Obtiene el elemento que se clickeó
        var a = new i(e); // Crea un nuevo objeto Sharer
        a.share(); // Llama al método share()
    };

    // Métodos de la clase Sharer
    i.prototype = {
        constructor: i,

        // Obtiene un atributo data-*
        getValue: function (t, e) {
            e = e === undefined ? "" : e; // Valor por defecto
            var a = this.elem.getAttribute("data-" + t);
            return a === undefined || a === null ? e : a;
        },

        // Lógica principal para compartir
        share: function () {
            var t = this.getValue("sharer").toLowerCase(); // Nombre de la red (ej. "facebook")

            // Lista de redes y sus URLs base + parámetros
            var e = {
                facebook: {
                    shareUrl: "https://www.facebook.com/sharer/sharer.php",
                    params: { u: this.getValue("url") }
                },
                googleplus: {
                    shareUrl: "https://plus.google.com/share",
                    params: { url: this.getValue("url") }
                },
                linkedin: {
                    shareUrl: "https://www.linkedin.com/shareArticle",
                    params: { url: this.getValue("url"), mini: true }
                },
                twitter: {
                    shareUrl: "https://twitter.com/intent/tweet/",
                    params: {
                        text: this.getValue("title"),
                        url: this.getValue("url"),
                        hashtags: this.getValue("hashtags"),
                        via: this.getValue("via")
                    }
                },
                email: {
                    shareUrl: "mailto:" + this.getValue("to"),
                    params: {
                        subject: this.getValue("subject"),
                        body: this.getValue("title") + "\n" + this.getValue("url")
                    },
                    isLink: true
                },
                whatsapp: {
                    shareUrl: "whatsapp://send",
                    params: { text: this.getValue("title") + " " + this.getValue("url") },
                    isLink: true
                },
                telegram: {
                    shareUrl: "tg://msg_url",
                    params: { text: this.getValue("title") + " " + this.getValue("url") },
                    isLink: true
                },
                viber: {
                    shareUrl: "viber://forward",
                    params: { text: this.getValue("title") + " " + this.getValue("url") },
                    isLink: true
                },
                line: {
                    shareUrl: "http://line.me/R/msg/text/?" +
                        encodeURIComponent(this.getValue("title") + " " + this.getValue("url")),
                    isLink: true
                },
                pinterest: {
                    shareUrl: "https://www.pinterest.com/pin/create/button/",
                    params: {
                        url: this.getValue("url"),
                        media: this.getValue("image"),
                        description: this.getValue("description")
                    }
                },
                tumblr: {
                    shareUrl: "http://tumblr.com/widgets/share/tool",
                    params: {
                        canonicalUrl: this.getValue("url"),
                        content: this.getValue("url"),
                        posttype: "link",
                        title: this.getValue("title"),
                        caption: this.getValue("caption"),
                        tags: this.getValue("tags")
                    }
                },
                hackernews: {
                    shareUrl: "https://news.ycombinator.com/submitlink",
                    params: { u: this.getValue("url"), t: this.getValue("title") }
                },
                reddit: {
                    shareUrl: "https://www.reddit.com/submit",
                    params: { url: this.getValue("url") }
                },
                vk: {
                    shareUrl: "http://vk.com/share.php",
                    params: {
                        url: this.getValue("url"),
                        title: this.getValue("title"),
                        description: this.getValue("caption"),
                        image: this.getValue("image")
                    }
                },
                xing: {
                    shareUrl: "https://www.xing.com/app/user",
                    params: { op: "share", url: this.getValue("url"), title: this.getValue("title") }
                },
                buffer: {
                    shareUrl: "https://buffer.com/add",
                    params: {
                        url: this.getValue("url"),
                        title: this.getValue("title"),
                        via: this.getValue("via"),
                        picture: this.getValue("picture")
                    }
                },
                instapaper: {
                    shareUrl: "http://www.instapaper.com/edit",
                    params: {
                        url: this.getValue("url"),
                        title: this.getValue("title"),
                        description: this.getValue("description")
                    }
                },
                pocket: {
                    shareUrl: "https://getpocket.com/save",
                    params: { url: this.getValue("url") }
                },
                digg: {
                    shareUrl: "http://www.digg.com/submit",
                    params: { url: this.getValue("url") }
                },
                stumbleupon: {
                    shareUrl: "http://www.stumbleupon.com/submit",
                    params: { url: this.getValue("url"), title: this.getValue("title") }
                },
                flipboard: {
                    shareUrl: "https://share.flipboard.com/bookmarklet/popout",
                    params: {
                        v: 2,
                        title: this.getValue("title"),
                        url: this.getValue("url"),
                        t: Date.now()
                    }
                },
                weibo: {
                    shareUrl: "http://service.weibo.com/share/share.php",
                    params: {
                        url: this.getValue("url"),
                        title: this.getValue("title"),
                        pic: this.getValue("image"),
                        appkey: this.getValue("appkey"),
                        ralateUid: this.getValue("ralateuid"),
                        language: "zh_cn"
                    }
                },
                renren: {
                    shareUrl: "http://share.renren.com/share/buttonshare",
                    params: { link: this.getValue("url") }
                },
                myspace: {
                    shareUrl: "https://myspace.com/post",
                    params: {
                        u: this.getValue("url"),
                        t: this.getValue("title"),
                        c: this.getValue("description")
                    }
                },
                blogger: {
                    shareUrl: "https://www.blogger.com/blog-this.g",
                    params: {
                        u: this.getValue("url"),
                        n: this.getValue("title"),
                        t: this.getValue("description")
                    }
                },
                baidu: {
                    shareUrl: "http://cang.baidu.com/do/add",
                    params: { it: this.getValue("title"), iu: this.getValue("url") }
                },
                douban: {
                    shareUrl: "https://www.douban.com/share/service",
                    params: {
                        name: this.getValue("title"),
                        href: this.getValue("url"),
                        image: this.getValue("image")
                    }
                },
                okru: {
                    shareUrl: "https://connect.ok.ru/dk",
                    params: {
                        "st.cmd": "WidgetSharePreview",
                        "st.shareUrl": this.getValue("url"),
                        title: this.getValue("title")
                    }
                },
                mailru: {
                    shareUrl: "http://connect.mail.ru/share",
                    params: {
                        share_url: this.getValue("url"),
                        linkname: this.getValue("title"),
                        linknote: this.getValue("description"),
                        type: "page"
                    }
                }
            };

            // Obtiene la configuración de la red actual
            var a = e[t];
            if (a) {
                a.width = this.getValue("width");
                a.height = this.getValue("height");
            }
            return a !== undefined ? this.urlSharer(a) : false;
        },

        // Construye la URL final y abre la ventana o enlace
        urlSharer: function (t) {
            var e = t.params || {},
                a = Object.keys(e),
                r,
                i = a.length > 0 ? "?" : "";

            // Construye la query string con encodeURIComponent
            for (r = 0; r < a.length; r++) {
                if (i !== "?") { i += "&"; }
                if (e[a[r]]) {
                    i += a[r] + "=" + encodeURIComponent(e[a[r]]);
                }
            }

            // Añade parámetros a la URL base
            t.shareUrl += i;

            if (!t.isLink) {
                // Si no es un enlace directo, abre ventana emergente
                var s = t.width || 600,
                    l = t.height || 480,
                    h = o.innerWidth / 2 - s / 2 + o.screenX,
                    u = o.innerHeight / 2 - l / 2 + o.screenY,
                    n = "scrollbars=no, width=" + s + ", height=" + l +
                        ", top=" + u + ", left=" + h,
                    g = o.open(t.shareUrl, "", n);
                if (o.focus) { g.focus(); }
            } else {
                // Si es un enlace directo (ej. WhatsApp, Telegram, Email)
                o.location.href = t.shareUrl;
            }
        }
    };

    // Inicializa cuando la página carga
    if (r.readyState === "complete" || r.readyState !== "loading") {
        i.init();
    } else {
        r.addEventListener("DOMContentLoaded", i.init);
    }

    // Re-inicializa en eventos page:load (para SPA)
    o.addEventListener("page:load", i.init);

    // Expone la clase globalmente
    o.Sharer = i;

})(window, document);
