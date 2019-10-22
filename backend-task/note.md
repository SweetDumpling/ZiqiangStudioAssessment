## 学习笔记

在项目过程中，遇到了 ajax 与 django 模板同时使用的问题，在网上参考了几篇文章后，得到了解决方案。

需求：用户选择搜索的项目类型，输入关键字，点击搜索按钮，即可得到符合条件的所有条目。

我们首先得有选择框、输入框和搜索按钮供用户使用：

```html
<select id="search-select">
    <option value="page_title">公告页面标题</option>
    <option value="title">讲座标题</option>
    <option value="speaker">主讲人</option>
    <option value="time">讲座时间</option>
    <option value="room">讲座地点</option>
    <option value="announce_date">公告发布时间</option>
</select>
<input id="search-input" placeholder="请输入搜索内容" type="text">
<button type="button" onclick="search()">搜索</button>
```

然后在 `search()` 中实现 Ajax ，以向服务器发送请求，并且部分刷新网页中列表的部分：

```javascript
function search() {
    var xhr;
    if (window.XMLHttpRequest) {
        xhr = new XMLHttpRequest();
    } else {
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            //<刷新网页内容>
        }
    }
    //<获得select和input的内容>
    //...（检查input的内容）
    xhr.open("GET", /*<url>*/, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send();
}
```

&lt;获得select和input的内容&gt; =

```javascript
var select = document.getElementById("search-select").value;
var input = document.getElementById("search-input").value;
```

之后将需要单独刷新的部分提到一个 HTML 文件（list.html）里：

```html
<ul>
    {% for lecture in LectureList %}
    <li>
        <a href="{{lecture.url}}">
            <strong>{{lecture.page_title}}</strong>
        </a>
        <span>({{lecture.announce_date}}发布)</span>
        <p>标题：{{lecture.title}}</p>
        <p>主讲人：{{lecture.speaker}}</p>
        <p>讲座时间：{{lecture.time}}</p>
        <p>讲座地点：{{lecture.room}}</p>
    </li>
    {% endfor %}
</ul>
```

当然要在原来的文件里 include 它，并且用一个 div 把它括起来。

```html
<div id="lecture-list-wrapper">
    {% include "list.html" %}
</div>
```

我们在 views.py 里添加对应的 `search()` 函数：

```python
def search(request, select, input):
    if select == 'page_title':
        lecture_list = # 根据input按page_title搜索
    elif select == 'title':
        lecture_list = # 根据input按title搜索
    elif select == 'speaker':
        # ...
    # ......
    else:
        lecture_list = Lecture.objects.all()
    # <render_to_string>
    return # <返回>
```

我们用 `search/?xxx=xxx&xxx=xxx` 的形式进行请求，在 urls.py 的 urlpatterns 里添加：

```python
path('search/', spider_views.search, name = 'search')
```

所以之前的&lt;url&gt; = `"{% url 'search' %}?select=" + select + "&input=" + input`

接下来是解决问题的关键点，如何刷新含有模板的部分网页呢？

我参考了[这篇文章](https://www.jianshu.com/p/8ba6e716d223)，它使用了一个叫做 `render_to_string()` 的函数：

&lt;render_to_string&gt; =

```python
lecture_list_rendering = render_to_string("list.html", {"LectureList": lecture_list })
```

它将 list.html 单独进行渲染，并且输出 HTML 字符串。然后以 JSON 格式返回状态信息和得到的字符串：

&lt;成功的返回&gt; =

```python
JsonResponse({'status': 'ok', 'lectureListRendering': lecture_list_rendering})
```

&lt;失败的返回&gt; =

```python
JsonResponse({'status': 'error'})
```

与之对应，&lt;刷新网页内容&gt; =

```javascript
responseObj = JSON.parse(xhr.responseText);
if (responseObj.status == 'ok') {
    document.getElementById("lecture-list-wrapper").innerHTML = responseObj.lectureListRendering;
} else {
    alert("Search failed.")
}
```

如果返回的 status 为 ok ，则刷新之前括起来的部分，使其 innerHTML 为之前得到的 HTML 字符串。这样就实现了单独刷新包含模板的部分网页的功能。


不过它为什么要使用 `render_to_string()` 而不是 `render()` 呢？

官网关于 `render()` 的说法：

> It’s a very common idiom to load a template, fill a context and return an HttpResponse object with the result of the rendered template. Django provides a shortcut. 

> The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

实际上，

```python
def index(request):
    return render(request, 'index.html', {'LectureList': Lecture.objects.all()})
```

是

```python
def index(request):
    template = loader.get_template('index.html')
    context = {'LectureList': Lecture.objects.all()}
    return HttpResponse(template.render(context, request))
```

的简化。

观察包名，我们发现 `render()` 属于 `django.shortcuts` 。而这里我们用到的 `render_to_string()` 属于 `django.templates.loader` 。推测 `render_to_string()` 大概是 `render()` 内部调用的函数，django 在 shortcuts.py 里的源码印证了这一推测：

```python
def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
```

所以

```python
def index(request):
    return render(request, 'index.html', {'LectureList': Lecture.objects.all()})
```

和

```python
def index(request):
    content = render_to_string("index.html", {'LectureList': Lecture.objects.all()}, request)
    return HttpResponse(content)
```

是等价的。

得出结论，`render()` 是渲染模板的函数的一个简化版本，像是一个封装，不过实际上其内部直接调用了 `render_to_string()` 。这篇文章所做的，实际上是重写的一遍 `render()` 的内容，只不过将返回值由 HttpResponse 换成了 JsonResponse 。我们的 search 功能理论上不会出问题，所以我不打算返回 status。于是修改代码：

&lt;返回&gt; =

```python
render(request, 'list.html', {"LectureList": lecture_list})
```

去掉&lt;render_to_string&gt;

&lt;刷新网页内容&gt; =

```javascript
document.getElementById("lecture-list-wrapper").innerHTML = xhr.responseText;
```

可以看出代码也简化了很多。

以上便是 ajax 刷新含有 django 模板的部分网页的方法。整体的思路是，将刷新的部分网页的独立成 HTML 文件，用 `render()` 或 `render_to_string()` 再渲染一次，然后将渲染结果发送给浏览器，赋给包含了该部分网页的 div 的 innerHTML。