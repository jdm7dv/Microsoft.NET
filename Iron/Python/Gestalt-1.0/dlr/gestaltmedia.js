if (typeof HTMLElement != "undefined" && !HTMLElement.prototype.insertAdjacentElement) {
    HTMLElement.prototype.insertAdjacentElement = function (where, parsedNode) {
        switch (where) {
            case 'beforeBegin':
                this.parentNode.insertBefore(parsedNode, this)
                break;
            case 'afterBegin':
                this.insertBefore(parsedNode, this.firstChild);
                break;
            case 'beforeEnd':
                this.appendChild(parsedNode);
                break;
            case 'afterEnd':
                if (this.nextSibling)
                    this.parentNode.insertBefore(parsedNode, this.nextSibling);
                else this.parentNode.appendChild(parsedNode);
                break;
        }
    }
}

if (!window.GestaltMedia) {
    window.GestaltMedia = {};
    GestaltMedia.__objectCount = 1;
}

if (!GestaltMedia.__loaded) {
    // we need to pause until DLR is done loading
    GestaltMedia.__startup = function () {
        if (!window.DLR || DLR.__loaded != true)
            setTimeout(GestaltMedia.__startup, 1000);
        else
            GestaltMedia.Run();
    }

    GestaltMedia.Run = function() {

        var mediatags = []

        var videotags = document.getElementsByTagName("video");
        var audiotags = document.getElementsByTagName("audio");

        for (videoidx = 0; videoidx < videotags.length; videoidx++) mediatags.push(videotags[videoidx]);
        for (audioidx = 0; audioidx < audiotags.length; audioidx++) mediatags.push(audiotags[audioidx]);

        var nodes = []



        for (mediaidx = 0; mediaidx < mediatags.length; mediaidx++) {

            var tag = mediatags[mediaidx];

            if (tag.tagName == "AUDIO" && navigator.userAgent.indexOf("Chrome") != -1) {
                continue;
            }

            var settings = GestaltMedia.parseMediaTag(tag);
            GestaltMedia.InjectSettingsXml(tag, settings);
            var xamltag = GestaltMedia.InjectXamlRef(tag, settings);
            nodes.push(settings);
            tag.style.display = "none";
        }
        GestaltMedia.InjectScriptTagAndActivate(nodes);
    }

    GestaltMedia.parseMediaTag = function (tag) {
        settings = {}
        settings.sources = []

        if (tag.tagName == "VIDEO") settings["video"] = "true";
        else settings["video"] = "false";
        
        var attributes = ["id", "width", "height", "skin", "autoplay", "volume", "poster", "loop", "controls", "autobuffer", "muted"];

        for (attidx = 0; attidx < attributes.length; attidx++) {
            var attval = tag.getAttribute(attributes[attidx]);
            if (attval != null) {
                settings[attributes[attidx]] = attval;
            }
        }

        if (tag.children.length > 0) {
            // using chrome or FF
            for (i = 0; i < tag.children.length; i++) {
                var srctag = tag.children[i];
                var srcval = srctag.getAttribute("src");
                if (srcval != null) {
                    settings.sources.push(srcval);
                }
            }
        }
        else {
            // using IE
            var srctag = tag.nextSibling;
            while (srctag.tagName == "SOURCE" || srctag.tagName == "/SOURCE") {
                if (srctag.tagName == "SOURCE") {
                    var srcval = srctag.getAttribute("src");
                    if (srcval != null) {
                        settings.sources.push(srcval);
                    }
                }
                srctag = srctag.nextSibling;
            }
        }

        if (settings.id == null) {
            settings.id = "gestaltmedia" + GestaltMedia.__objectCount;
            GestaltMedia.__objectCount++;
        }

        settings.xamlid = settings.id + "-xaml";
        settings.settingsid = settings.id + "-settings";

        return settings;
    }

    GestaltMedia.InjectSettingsXml = function (tag, settings) {
        var settingsXml = GestaltMedia.ToXml(settings);
        var scriptTag = document.createElement("script");
        scriptTag.type = "text/xml";
        scriptTag.id = settings.settingsid;
        scriptTag.text = settingsXml;
        tag.insertAdjacentElement('afterEnd', scriptTag);

        return scriptTag;
    }

    GestaltMedia.InjectXamlRef = function (tag, settings) {
        var scriptTag = document.createElement("script");
        scriptTag.type = "application/xml+xaml";
        scriptTag.id = settings.xamlid;


        if (settings.width != null) scriptTag.setAttribute("width", settings.width);
        if (settings.height != null) scriptTag.setAttribute("height", settings.height);

        if (settings.skin != null) {
            scriptTag.src = settings.skin;
        }
        else {
            if (settings.video == "true") scriptTag.src = "video.xaml";
            else scriptTag.src = "audio.xaml";
        }
        tag.insertAdjacentElement('afterEnd', scriptTag);

        return scriptTag;
    }

    GestaltMedia.InjectScriptTagAndActivate = function (nodes) {
        // add the script tag, call DLR activations
        var scriptTag = document.createElement("script");
        scriptTag.type = "text/python";
        scriptTag.src = "media.py";

        var classval = "";
        for (i = 0; i < nodes.length; i++) {
            classval += nodes[i].xamlid;
            if (i != nodes.length - 1) classval += ", ";
        }

        if (navigator.appName == "Microsoft Internet Explorer") {
            scriptTag.className = classval;
        }
        else {
            scriptTag.setAttribute("class", classval);
        }

        document.body.appendChild(scriptTag); // this will be at end of document, which could be an issue

        // TODO: Now loop through all of the nodes and call DLR.createSilverlightObject
        for (i = 0; i < nodes.length; i++) {
            // need to translate gestalt settings to dlr settings
            var gsettings = nodes[i];
            var settings = {}; // this is in dlr format
            if (gsettings.width != null) settings.width = gsettings.width;
            if (gsettings.height != null) settings.height = gsettings.height;
            if (gsettings.xamlid != null) settings.xamlid = gsettings.xamlid;

            DLR.__createSilverlightObject(nodes[i].xamlid, DLR.parseSettings(DLR.getSettings(), settings));
        }

        return scriptTag;
    }

    GestaltMedia.ToXml = function (settings) {
        var settingsXml = "<settings>\r\n";
        for (var attr in settings) {
            if (attr != "sources") {
                settingsXml += "<" + attr + ">";
                settingsXml += GestaltMedia.XmlEncode(settings[attr]);
                settingsXml += "</" + attr + ">\r\n";
            }
        }
        settingsXml += "<sources>";
        for (i = 0; i < settings.sources.length; i++) {
            settingsXml += "<source>" + GestaltMedia.XmlEncode(settings.sources[i]) + "</source>\r\n";
        }
        settingsXml += "</sources>\r\n";
        settingsXml += "</settings>";
        return settingsXml;
    }

    GestaltMedia.XmlEncode = function (val) {
        val = val.replace("&", "&amp;");
        val = val.replace("<", "&lt;");
        val = val.replace(">", "&gt;");
        val = val.replace("'", "&apos;");
        val = val.replace('"', "&quot;");
        return val;
    }

    GestaltMedia.__loaded = true;
}

if(window.addEventListener) {
    window.addEventListener('load', GestaltMedia.__startup, false);
} else {
    window.attachEvent('onload', GestaltMedia.__startup);
}