import { BACKEND_PORT } from "./config.js";
import { fileToDataUrl, logout, isLoggedIn } from "./helpers.js";
import { changeHash } from "./router.js";
import { pollNotifications } from "./router.js";
pollNotifications();

function renderNavBar() {
    var authFlag = isLoggedIn();
    console.log(authFlag)
    const navBrand = document.createElement("a");
    navBrand.setAttribute("class", "navbar-brand d-flex");

    const logo = document.createElement("img");
    logo.setAttribute("class", "btn p-0 me-2");
    logo.src = "../img/l4w_big.png";
    logo.alt = "L4W";
    logo.width = 120;
    logo.height = 40;

    navBrand.appendChild(logo);

    var nav = document.getElementById("navbar");

    var newNav = document.createElement("nav");
    newNav.setAttribute("class", "navbar navbar-expand-lg bg-body-tertiary");
    newNav.setAttribute("id", "navbar");

    var navContainerDiv = document.createElement("div");
    navContainerDiv.setAttribute("class", "container-fluid");

    var div = document.createElement("div");
    div.setAttribute("class", "collapse navbar-collapse");
    div.setAttribute("id", "navbarSupportedContent");

    var dropButton = document.createElement("navbar-toggler");
    dropButton.setAttribute("class", "navbar-toggler");
    dropButton.setAttribute("type", "button");
    dropButton.setAttribute("data-bs-toggle", "collapse");
    dropButton.setAttribute("data-bs-target", "#navbarSupportedContent");
    dropButton.setAttribute("aria-controls", "navbarSupportedContent");
    dropButton.setAttribute("aria-expanded", "false");
    dropButton.setAttribute("aria-label", "Toggle navigation");

    var toggleIcon = document.createElement("span");
    toggleIcon.setAttribute("class", "navbar-toggler-icon h3");
    toggleIcon.innerText = ". . .";

    dropButton.appendChild(toggleIcon);

    newNav.appendChild(navContainerDiv);
    navContainerDiv.appendChild(navBrand);
    navContainerDiv.appendChild(dropButton);
    navContainerDiv.appendChild(div);

    var linkList = document.createElement("ul");
    linkList.setAttribute(
        "class",
        "navbar-nav ms-auto mb-2 mb-lg-0 text-end pe-0"
    );
    div.appendChild(linkList);

    if (authFlag) {
        authNav(navBrand, linkList);
        logo.addEventListener("click", () => changeHash("#home"));
    } else {
        noAuthNav(linkList);
        logo.addEventListener("click", () => changeHash(""));
    }

    nav.replaceWith(newNav);
}

function addLink(name, href, linkList) {
    var li = document.createElement("li");
    li.setAttribute("class", "nav-item pe-2 pt-1");
    linkList.appendChild(li);

    var link = document.createElement("a");
    link.href = href;
    link.setAttribute("class", "nav-link text-dark");
    link.textContent = name;
    li.appendChild(link);
}

// Navbar prior to logging in
function noAuthNav(linkList) {
    addLink("Join", "#join", linkList);
    addLink("Sign in", "#signin", linkList);
}

// Navbar when logged in
function authNav(navBrand, linkList) {
    var li1 = document.createElement("div");
    navBrand.appendChild(li1);

    var logoutButton = document.createElement("button");
    logoutButton.innerText = "Log out";
    logoutButton.setAttribute("class", "btn btn-danger p-1 pe-2 ps-2");
    li1.appendChild(logoutButton);
    logoutButton.addEventListener("click", function (event) {
        logout();
        changeHash("#welcome");
        location.reload();
    });

    addLink("Home", "#home", linkList);
    addLink("Me", "#me", linkList);

    var notificationLi = document.createElement("li");
    notificationLi.setAttribute("class", "nav-item pt-1 pb-1");
    linkList.appendChild(notificationLi);

    var notificationButton = document.createElement("button");
    notificationButton.setAttribute(
        "class",
        "btn btn-primary position-relative me-2"
    );
    notificationButton.innerText = "Notifications";
    notificationButton.setAttribute("data-bs-toggle", "offcanvas");
    notificationButton.setAttribute("data-bs-target", "#notificationsOffcanvas");
    notificationButton.setAttribute("aria-controls", "notificationsOffcanvas");
    notificationLi.appendChild(notificationButton);
}

export { renderNavBar };
