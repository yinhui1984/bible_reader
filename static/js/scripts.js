
var guildlineData = null;

initBookGuildline();

document.getElementById("btn_next").addEventListener("click", function () {
    let bookSelectControl = document.getElementById("book_select");
    let bookName = bookSelectControl.value;
    let charpterSelectControl = document.getElementById("charpter_select");
    let charpterIndex = charpterSelectControl.value;

    if (bookName === '' || charpterIndex === '') {
        return;
    }

    let nextCharpterIndex = parseInt(charpterIndex) + 1;

    // get max charpter index from guildlineData
    for (let book of guildlineData.books) {
        if (book.bookName === bookName) {
            if (nextCharpterIndex > book.maxCharpterIndex) {
                // change book 
                let nextBookIndex = guildlineData.books.indexOf(book) + 1;
                if (nextBookIndex >= guildlineData.books.length) {
                    nextBookIndex = 0;
                }
                bookSelectControl.value = guildlineData.books[nextBookIndex].bookName;
                charpterSelectControl.value = 1;
                loadBookContent();
                return
            }
        }
    }


    charpterSelectControl.value = nextCharpterIndex;
    loadBookContent();
});

function loadBookContentWithLastStatus() {
    fetch('/last', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            let bookName = data.bookName;
            let charpterIndex = data.charpterIndex;

            bookSelectControl = document.getElementById("book_select");
            bookSelectControl.value = bookName;

            charpterSelectControl = document.getElementById("charpter_select");
            charpterSelectControl.value = charpterIndex;

            loadBookContent();
        });
}


function initBookGuildline() {

    fetch('/guildline', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            guildlineData = data;
            updateBookSelect();
            updateCharpterSelect();
            loadBookContentWithLastStatus();
        });
}



function updateBookSelect() {
    bookSelectControl = document.getElementById("book_select");
    bookSelectControl.innerHTML = '';
    for (let book of guildlineData.books) {
        bookSelectControl.options.add(new Option(book.bookName, book.bookName));
    }


    bookSelectControl.removeEventListener("change", updateCharpterSelect);
    bookSelectControl.removeEventListener("change", loadBookContent);
    bookSelectControl.addEventListener("change", updateCharpterSelect);
    bookSelectControl.addEventListener("change", loadBookContent);
}


function updateCharpterSelect() {
    bookSelectControl = document.getElementById("book_select");
    let bookName = bookSelectControl.value;
    charpterSelectControl = document.getElementById("charpter_select");
    charpterSelectControl.innerHTML = '';

    for (let book of guildlineData.books) {
        if (book.bookName === bookName) {
            for (let i = 1; i <= book.maxCharpterIndex; i++) {
                charpterSelectControl.options.add(new Option(i, i));
            }
            break;
        }
    }

    charpterSelectControl.removeEventListener("change", loadBookContent)
    charpterSelectControl.addEventListener("change", loadBookContent)
}

function loadBookContent() {
    bookSelectControl = document.getElementById("book_select");
    let bookName = bookSelectControl.value;
    charpterSelectControl = document.getElementById("charpter_select");
    let charpterIndex = charpterSelectControl.value;

    if (bookName === '' || charpterIndex === '') {
        return;
    }

    fetch('/content?bookName=' + bookName + '&charpterIndex=' + charpterIndex, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            createContent(data.verses);
        });
}



function createContent(content) {

    let contentDiv = document.getElementById("current_content");
    // clear it first
    contentDiv.innerHTML = '';

    content.forEach((element, index) => {
        let p = document.createElement("p");

        let chapterNumber = element.chapter;
        let text = element.content;
        let note = element.note;  // 获取注释

        let spanChapterIndex = document.createElement("span");
        spanChapterIndex.className = "chapter-number text-opacity-75 text-secondary text-nowrap";
        spanChapterIndex.innerText = chapterNumber;

        let spanChapterText = document.createElement("span");
        spanChapterText.className = "text-content";
        spanChapterText.innerText = text;


        p.appendChild(spanChapterIndex);
        p.appendChild(document.createTextNode(' '));  // 添加一个空格
        p.appendChild(spanChapterText);

        // 如果注释不为空，则更改样式并添加 collapse
        if (note.trim() !== "") {
            let collapseID = 'collapseNote' + index;  // 为每个 collapse 创建一个唯一的 ID

            // 设置 Bootstrap 特定的属性以启用 collapse
            spanChapterIndex.setAttribute("data-bs-toggle", "collapse");
            spanChapterIndex.setAttribute("data-bs-target", '#' + collapseID);
            spanChapterIndex.classList.add("text-decoration-underline");  // 添加下划线以表示有注释
            // 设置鼠标指针
            spanChapterIndex.style.cursor = 'pointer';

            let divCollapse = document.createElement('div');
            divCollapse.id = collapseID;
            divCollapse.className = 'collapse text-secondary text-opacity-75 ';
            // outline: 1px dashed
            divCollapse.style.outline = '1px dashed';
            divCollapse.innerText = note;

            p.appendChild(divCollapse);  // 将 collapse div 添加到 p 元素中
        }



        contentDiv.appendChild(p);
        window.scrollTo(0, 0);
    });



}



