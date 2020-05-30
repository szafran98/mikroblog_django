function time2TimeAgo(ts) {


    let d = new Date();
    let nowTs = d.getTime() / 1000;
    let seconds = nowTs - ts;

    // more that two days
    if (seconds > 30 * 24 * 3600) {
        return Math.floor(seconds / (30 * 24 * 3600)) + " months ago";
    }
    // a day
    if (seconds > 7 * 24 * 3600) {
        return Math.floor(seconds / (7 * 24 * 3600)) + " weeks ago";
    }

    if (seconds > 24 * 3600) {
        return Math.floor(seconds / (24 * 3600)) + " days ago";
    }
    if (seconds > 3600) {
        return Math.floor(seconds / 3600) + " hours ago";
    }
    if (seconds > 60) {
        return Math.floor(seconds / 60) + " minutes ago";
    }
    if (seconds < 60) {
        return "Less than a minute";
    }

}


let entryId;
let array = [];

function dropDownPost(author, postId) {

    if (array.length >= 1) {
        document.querySelector(array[0]).classList.remove("show");
        array.pop();
    }
    let username;
    if (author instanceof HTMLCollection) {
        username = author[0].classList[1];
    } else {
        username = author.id;
    }
    let post = 'entry' + postId;


    let selector = `div.myDropdown.${username}.${post}`;
    document.querySelector(`div.myDropdown.${username}.${post}`).classList.toggle("show");

    array.push(selector);
    entryId = postId;

}

function dropDownComment(author, commentId) {
    if (array.length >= 1) {
        document.querySelector(array[0]).classList.remove("show");
        array.pop();
    }


    let comment = 'entry' + commentId;
    let username = author[0].id;
    let selector = `div.myDropdown.${username}.${comment}`;
    document.querySelector(`div.myDropdown.${username}.${comment}`).classList.toggle("show");

    array.push(selector);
    entryId = commentId;

}

window.onclick = function (event) {

    if (!document.getElementsByClassName(`autorwpisu${entryId}`)[0].contains(event.target)) {
        let dropdowns = document.getElementsByClassName(`entry${entryId} dropdown-content`);
        //let i;
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}


window.onload = () => {
    let allTimesToChange = document.querySelectorAll('time');
    allTimesToChange.forEach((element) => {
        let timeToChange = element.innerHTML;
        let toNumber = parseInt(timeToChange);
        element.innerHTML = time2TimeAgo(toNumber);
    });

}

