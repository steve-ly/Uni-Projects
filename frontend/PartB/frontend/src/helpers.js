import { renderError } from "./router.js"

/**
 * Given a js file object representing a jpg or png image, such as one taken
 * from a html file input element, return a promise which resolves to the file
 * data as a data url.
 * More info:
 *   https://developer.mozilla.org/en-US/docs/Web/API/File
 *   https://developer.mozilla.org/en-US/docs/Web/API/FileReader
 *   https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
 * 
 * Example Usage:
 *   const file = document.querySelector('input[type="file"]').files[0];
 *   console.log(fileToDataUrl(file));
 * @param {File} file The file to be read.
 * @return {Promise<string>} Promise which resolves to the file as a data url.
 */

import { BACKEND_PORT } from './config.js';

let feedLength = 0;
let feedData = [];


export function fileToDataUrl(file) {
    const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg']
    const valid = validFileTypes.find(type => type === file.type);
    // Bad data, let's walk away.
    if (!valid) {
        throw Error('provided file is not a png, jpg or jpeg image.');
    }

    const reader = new FileReader();
    const dataUrlPromise = new Promise((resolve, reject) => {
        reader.onerror = reject;
        reader.onload = () => resolve(reader.result);
    });
    reader.readAsDataURL(file);
    return dataUrlPromise;
}
export const PORT = BACKEND_PORT
export const PORT_frontend = 8000


//check if logged in 
export function isLoggedIn() {
    if (localStorage.getItem("token") == null || localStorage.getItem("token") == undefined) {
        return false;
    }
    return true;
}

//logout user
export function logout() {
    localStorage.clear();
}

//Sends fetch to log user in 
export function login(email, password) {
    var loginForm = {
        "email": email,
        "password": password
    }
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:${PORT}/auth/login`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginForm),
        })
            .then((response) => { console.log(response); return response.json(); })
            .then(data => {
                if (data['error']) {
                    resolve(data);
                } else {
                    localStorage.setItem("token", data['token']);
                    localStorage.setItem("currentUser", data['userId']);
                    resolve(data);
                }
            })
            .catch((error) => {
                renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");
                console.error('Error:', error);
            });
    });

}

//Sends fetch to register users 
export function register(email, password, name) {
    var registerForm = {
        "email": email,
        "password": password,
        "name": name
    }
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:${PORT}/auth/register`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registerForm),
        })
            .then((response) => response.json())
            .then(data => {
                if (data['error']) {
                    resolve(data);
                } else {
                    localStorage.setItem("token", data['token']);
                    localStorage.setItem("currentUser", data['userId']);
                    resolve(data);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");
            });
    });

}

//gets the feed for page index start
export function getFeed(start) {
    const userToken = localStorage.getItem("token");
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:${PORT}/job/feed?start=${start}`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + userToken,
                'Accept': 'application/json'
            },
        })
            .then((response) => response.json())
            .then(data => {
                if (data['error']) {
                    resolve(data);
                } else {
                    if (start <= 15) { //saves a max of 15 jobs
                        localStorage.setItem(`jobFeed-${start}`, JSON.stringify(data));
                    }
                    resolve(data);
                }
            })
            .catch((error) => {
                reject(error);
            });
    });
}

//get how many jobs the user has in their feed
export function getFeedLength() {
    const userToken = localStorage.getItem("token");
    var data = null;
    var count = 0;
    var pageIndex = 0;
    return new Promise((resolve, reject) => {
        function getNextFeed(pageIndex) {
            fetch(`http://localhost:${PORT}/job/feed?start=${feedLength}`, {
                method: "GET",
                headers: {
                    Authorization: "Bearer " + userToken,
                    Accept: "application/json",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.length == 0) {
                        resolve();
                    } else {
                        let notificationData = {
                            "creatorId": data[0].creatorId,
                            "title": data[0].title,
                            "createdAt": data[0].createdAt
                        };

                        feedData.push(notificationData);
                        feedLength = feedLength + 1;
                        getNextFeed(feedLength);
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        }
        getNextFeed(0);
        localStorage.setItem("feedLength", feedLength);
        localStorage.setItem("feedData", JSON.stringify(feedData));

    });
}

//sends fetch request to like job
export function likeJob(jobId, likeState) {
    const userToken = localStorage.getItem("token");
    const likeJob = {
        "id": jobId,
        "turnon": likeState,
    }
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:${PORT}/job/like`, {
            method: 'PUT',
            headers: {
                'Authorization': 'Bearer ' + userToken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(likeJob),
        })
            .then((response) => response.json())
            .then(data => {
                if (data['error']) {
                    resolve(data);
                } else {
                    resolve(data);

                }
            })
            .catch((error) => {
                renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");
            });
    });
}

//sends fetch to add job
export function addJob(title, image, start, description) {
    const userToken = localStorage.getItem("token");
    const jobDesc = {
        "title": title,
        "image": image,
        "start": start,
        "description": description

    }
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:${PORT}/job`, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + userToken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jobDesc),
        })
            .then((response) => response.json())
            .then(data => {
                if (data['error']) {
                    resolve(data);
                } else {
                    resolve(data);
                }
            })
            .catch((error) => {
                renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");
                console.error('Error:', error);
            });
    });
}

//sends fetch to update job
export function putJob(jobId, title, image, start, description) {
    const userToken = localStorage.getItem("token");
    const jobDesc = {
        "id": jobId,
        "title": title,
        "image": image,
        "start": start,
        "description": description
    }
    fetch(`http://localhost:${PORT}/job`, {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + userToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jobDesc),
    })
        .then((response) => response.json())
        .then(data => {
            if (data['error']) {
                renderError(data['error'])
                return false;
            } else {
                return true;

            }
        })
        .catch((error) => {
            renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");
        });
}

//sends fetch to delete job
export function deleteJob(jobId) {
    const userToken = localStorage.getItem("token");
    const id = {
        "id": jobId,
    }
    fetch(`http://localhost:${PORT}/job`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + userToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(id),
    })
        .then((response) => response.json())
        .then(data => {
            if (data['error']) {
                return false;
            } else {
                return true;

            }
        })
        .catch((error) => {
            renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");
        });
}

//sends fetch to send a comment to job
export function commentJob(JobId, commentStr) {
    const userToken = localStorage.getItem("token");
    const comment = {
        "id": JobId,
        "comment": commentStr
    }
    fetch(`http://localhost:${PORT}/job/comment`, {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + userToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(comment),
    })
        .then((response) => response.json())
        .then(data => {
            if (data['error']) {
                renderError(data['error'])
                return false;
            } else {
                return true;

            }
        })
        .catch((error) => {
            renderError("Uh-oh! Theres currently an issue with the website, please wait a while then refresh the page or check your internet connection.");

        });
}

//sends fetch to get user information
export function getUser(userId) {
    const userToken = localStorage.getItem("token");
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:${PORT}/user?userId=${userId}`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + userToken,
                'Accept': 'application/json',
            },
        })
            .then((response) => response.json())
            .then(data => {
                resolve(data);
            })
            .catch((error) => {
                reject(error);
            });
    });
}


//sends fetch to update user
export function updateUser(email, password, name, image) { //validate
    const userToken = localStorage.getItem("token");
    const newUser = {
        "email": email,
        "password": password,
        "name": name,
        "image": image
    }
    fetch(`http://localhost:${PORT}/user`, {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + userToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newUser),
    })
        .then((response) => response.json())
        .then(data => {
            if (data['error']) {
                renderError(data['error']);
                return false;
            } else {
                return true;

            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

//sends fetch to watch user
export function watchUser(email, state) {
    const userToken = localStorage.getItem("token");
    const watching = {
        "email": email,
        "turnon": state,
    }

    fetch(`http://localhost:${PORT}/user/watch`, {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + userToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(watching),
    })
        .then((response) => response.json())
        .then(data => {
            if (data['error']) {
                renderError(data['error']);
                return false;
            } else {
                return true;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
