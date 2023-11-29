document.querySelector(".test").addEventListener('click', async () => {
    document.querySelector(".title_input").value == 0 ? alert("Title is blank") : 
    document.querySelector(".surname_input").value == 0 ? alert("Storage count is blank") :
    document.querySelector(".name_input").value == 0 ? alert("Author is blank") :
    document.querySelector(".patronymic_input").value == 0 ? alert("Author is blank") :
    document.querySelector(".due_input").value == 0 ? alert("Author is blank") : null
        const data = {
            book: document.querySelector(".title_input").value,
            surname: document.querySelector(".surname_input").value,
            name: document.querySelector(".name_input").value,
            patronymic: document.querySelector(".patronymic_input").value,
            due: document.querySelector(".due_input").value,
        };
        resp = await fetch("http://localhost:8000/give_process/post", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(data)
        })
        if (!resp.ok) {
            alert(`HTTP error: ${response.status}`)
        } else {
            alert('Successful')
        }
    }
)


document.querySelector(".b_sumbit").addEventListener('click', async () => {
    console.log(document.querySelector(".b_pic_input").value.slice(12, document.querySelector(".b_pic_input").value.length));
    document.querySelector(".b_title_input").value == 0 ? alert("Title is blank") : 
    document.querySelector(".b_storage_count_input").value == 0 ? alert("Storage count is blank") :
    document.querySelector(".b_author_input").value == 0 ? alert("Author is blank") :
    document.querySelector(".b_pic_input").value == 0 ? alert("Author is blank") : null
        const data = {  
            book: document.querySelector(".b_title_input").value,
            storage_count: document.querySelector(".b_storage_count_input").value,
            author: document.querySelector(".b_author_input").value,
            picture: `pictures\\${document.querySelector(".b_pic_input").value.slice(12, document.querySelector(".b_pic_input").value.length)}`,
        };
        console.log(data);
        resp = await fetch("http://localhost:8000/books/post", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(data)
        })
        if (!resp.ok) {
            alert(`HTTP error: ${response.status}`)
        } else {
            alert('Successful')
        }
    }
)


document.querySelector(".getProcess").addEventListener('click', async () => {
    resp = await fetch("http://localhost:8000/give_process/get")
    let allProcess = await resp.json()
    mainDiv = document.querySelector(".allProcess")
    console.log(allProcess);
    for (let i = 0; i < allProcess.length; i++) {
        div = document.createElement('div')
        id = document.createElement('p')
        id.innerHTML = allProcess[i][0]
        div.append(id)
        book = document.createElement('p')
        book.innerHTML = allProcess[i][1]
        div.append(book)
        reader = document.createElement('p')
        reader.innerHTML = allProcess[i][2]
        div.append(reader)
        date_given = document.createElement('p')
        date_given.innerHTML = allProcess[i][3]
        div.append(date_given)
        date_return = document.createElement('p')
        date_return.innerHTML = allProcess[i][4]
        div.append(date_return)
        returned = document.createElement('p')
        returned.innerHTML = allProcess[i][5]
        div.append(returned)
        days = document.createElement('p')
        days.innerHTML = allProcess[i][6]
        div.append(days)
        mainDiv.append(div)
        }
})

document.querySelector(".getBooks").addEventListener('click', async () => {
    resp = await fetch("http://localhost:8000/books/get")
    let allBooks = await resp.json()
    mainDiv = document.querySelector(".allBooks")
    console.log(allBooks);
    for (let i = 0; i < allBooks.length; i++) {
        div = document.createElement('div')
        id = document.createElement('p')
        id.innerHTML = allBooks[i][0]
        div.append(id)
        title = document.createElement('p')
        title.innerHTML = allBooks[i][1]
        div.append(title)
        storage_count = document.createElement('p')
        storage_count.innerHTML = allBooks[i][2]
        div.append(storage_count)
        author = document.createElement('p')
        author.innerHTML = allBooks[i][3]
        div.append(author)
        pic = document.createElement('img')
        console.log(allBooks[i][4].slice(5, allBooks[i][4].length));
        pic.src = allBooks[i][4].slice(5, allBooks[i][4].length)
        div.append(pic)
        mainDiv.append(div)
        }    
})