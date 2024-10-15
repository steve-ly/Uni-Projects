import { getFeed, likeJob, getUser, fileToDataUrl, commentJob, deleteJob, putJob } from './helpers.js';
import { changeHash, isValidDate, renderError, renderListModal, stopPolling } from "./router.js"

//Displays all jobs given the page index and state, where state is which page the user is rendering
export function displayFeed(index, state) {
    if (state == "home") { // displays the job feed at home page
        getFeed(index).then(data => {
            if (data["error"] == undefined) {
                var jobFeed = data;
                //If there are no job post then appends a placeholder container
                if (index == 0 && jobFeed.length == 0) {
                    const noPostsTemplate = document.getElementById("no-posts-container");
                    const noPostsClone = noPostsTemplate.content.cloneNode(true);
                    document.getElementById("main").appendChild(noPostsClone);
                    return;
                }
                //For all jobs in the data creates a job post
                for (let i = 0; i < jobFeed.length; i++) {
                    //call get user to retrieve creators name and picture
                    getUser(jobFeed[i].creatorId).then(data => {
                        if (data["error"] == undefined) {
                            const name = data.name;
                            const creatorPic = data.image;
                            generateJobPost(index, i, name, creatorPic, state, jobFeed);//create and append job post
                        }
                        else {
                            renderError(data["error"]);
                        }

                    })
                }
            }
            else {
                renderError(data['error']);
            }
        }).catch((error) => { //no connection
            stopPolling()
            var jobFeed = JSON.parse(localStorage.getItem(`jobFeed-${index}`));
            if (jobFeed != undefined && index < 16) {
                for (let i = 0; i < jobFeed.length; i++) {
                    //generate job without the creator name or image and use local storage
                    generateJobPost(index, i, "", "", state, jobFeed);
                }
            }

        });
    }
    //Displays all post made by the user, in this case index refers to userId
    else if (state == "profile") {
        getUser(index).then(data => {
            //If there are no job post then appends a placeholder container
            console.log(index);
            console.log(data.jobs.length);
            if (data.jobs.length == 0) {
                const noJobsTemplate = document.getElementById("no-jobs-container");
                const noJobsClone = noJobsTemplate.content.cloneNode(true);
                document.getElementById("user-jobs").appendChild(noJobsClone);
            }
            //Generates job post using user's post data from getUser fetch.
            for (let i = 0; i < data.jobs.length; i++) {
                const name = data.name;
                const creatorPic = data.image;
                generateJobPost(index, i, name, creatorPic, state, data);
            }
        })
    }
}

//Generates a job based on the:
//state: Which page the jobs will be rendering on
//index: A page index for when state is home and will be a userId when state is profile
//i index for which jobs within the index is being generated
//name and userImg are the creator's image
//data will be a json file.
export function generateJobPost(index, i, name, userImg, state, data) {
    var jobFeed;
    if (state == "home") {
        jobFeed = data;
    } else if (state == "profile") {
        jobFeed = data.jobs;
    }

    //initizalize properties of the job post.
    const role = jobFeed[i].title;
    var postTime = jobFeed[i].createdAt;
    const startDate = jobFeed[i].start;
    const about = jobFeed[i].description;
    const img = jobFeed[i].image;
    const comments = jobFeed[i].comments;
    const jobId = jobFeed[i].id;
    const creatorId = jobFeed[i].creatorId;
    const likes = jobFeed[i].likes;

    //creating DOM elements
    var jobPostContainer = document.createElement("div");
    jobPostContainer.setAttribute("class", "container");
    jobPostContainer.style = "max-width: 700px";
    jobPostContainer.setAttribute("id", `post-${jobId}`);

    var jobPostDiv1 = document.createElement("div");
    jobPostDiv1.setAttribute("class", "bg-white p-4 shadow mt-3");
    jobPostDiv1.style = "border-radius: 1rem;"

    var jobPostDiv2 = document.createElement("div");
    jobPostDiv2.setAttribute("class", "d-flex justify-content-between");

    //Adds an onclick event for creator details that will render page to the creator's user page
    var jobPostDiv3 = document.createElement("div");
    jobPostDiv3.setAttribute("class", "d-flex");
    jobPostDiv3.addEventListener("click", function (event) {
        event.preventDefault();
        changeHash(`#me=${creatorId}`)
    })

    var jobPostProfileImg = document.createElement("img");
    jobPostProfileImg.setAttribute("class", "rounded-circle me-2");
    jobPostProfileImg.src = userImg;
    jobPostProfileImg.alt = "profile-pic";
    jobPostProfileImg.style = "width: 38px; height: 38px;";

    var jobPostDiv4 = document.createElement("div");
    jobPostDiv4.setAttribute("class", "d-flex flex-column");

    var jobPostName = document.createElement("p");
    jobPostName.setAttribute("class", "btn m-0 p-0 fw-bold text-start");
    jobPostName.setAttribute("href", "#");
    jobPostName.innerText = name;

    //Get the creation date in hours and minutes
    var postTimetoDate = Date.parse(jobFeed[i].createdAt);
    var currentTime = new Date().getTime();
    var timePast = Math.floor((currentTime - postTimetoDate) / 1000);
    var hoursPassed = Math.floor(timePast / 3600);
    var minutesPassed = Math.floor((timePast % 3600) / 60);

    //format creation date
    if (timePast < 60) {
        postTime = "Posted less than a minute ago"
    } else if (hoursPassed < 24) {
        postTime = `Posted ${hoursPassed} hours and ${minutesPassed} minutes ago`;
    } else {
        var day = jobFeed[i].createdAt.substring(8, 10);
        var month = jobFeed[i].createdAt.substring(5, 7);
        var year = jobFeed[i].createdAt.substring(0, 4);
        postTime = `Posted ${day}/${month}/${year}`;
    }

    var jobPostTime = document.createElement("span");
    jobPostTime.setAttribute("class", "text-muted fs-7");
    jobPostTime.innerText = postTime;
    var jobPostEditDiv = document.createElement("div");

    var jobPostEditButton = document.createElement("button");
    jobPostEditButton.setAttribute("class", "ps-2 pe-2 btn btn-light pe-2 ps-2");
    jobPostEditButton.innerText = "Edit";
    jobPostEditButton.setAttribute("data-bs-toggle", "modal");
    jobPostEditButton.setAttribute("data-bs-target", "#editJobPostModal");
    jobPostEditButton.setAttribute("id", `edit-job-button-${jobId}`);


    //Adds event listener to the edit button
    jobPostEditButton.addEventListener("click", function (event) {
        document.getElementById("edit-job-post").addEventListener("click", function (event) {
            event.preventDefault();

            //get form inputs
            var editjobTitle = document.getElementById("editJobPost-role");
            var editjobDate = document.getElementById("editJobPost-date");
            var editjobDesc = document.getElementById("editJobPost-about");
            var editjobImg = document.getElementById("editJobPost-img");
            var validStatus = true;
            //resets invalid inputs
            editjobTitle.style.color = "";
            editjobTitle.style.border = "";
            document.getElementById("edit-role-label").innerText = "Role";
            document.getElementById("edit-role-label").style.color = "";

            editjobDate.style.color = "";
            editjobDate.style.border = "";
            document.getElementById("edit-start-label").innerText = "Start date";
            document.getElementById("edit-start-label").style.color = "";

            editjobDesc.style.color = "";
            editjobDesc.style.border = "";
            document.getElementById("edit-about-label").innerText = "About";
            document.getElementById("edit-about-label").style.color = "";



            //Check if inputs are valid, changes labels and border if not
            if (editjobTitle.value == "") {
                editjobTitle.style.color = "red";
                editjobTitle.style.border = "1px solid red";
                document.getElementById("edit-role-label").innerText = "Job must have a title";
                document.getElementById("edit-role-label").style.color = "red";
                validStatus = false;
            }
            if (editjobDate.value == "" || !isValidDate(editjobDate.value)) {
                editjobDate.style.color = "red";
                editjobDate.style.border = "1px solid red";
                document.getElementById("edit-start-label").innerText = "Invalid Starting date";
                document.getElementById("edit-start-label").style.color = "red";
                validStatus = false;
            }

            if (editjobDesc.value == "") {
                editjobDesc.style.color = "red";
                editjobDesc.style.border = "1px solid red";
                document.getElementById("edit-about-label").innerText = "Please add a description";
                document.getElementById("edit-about-label").style.color = "red";
                validStatus = false;
            }
            if (editjobImg.files[0] != undefined) {//if there is a file
                fileToDataUrl(editjobImg.files[0]).then((base64str) => {//change to base64
                    console.log(base64str);
                    if (validStatus == true) {//if the form was valid the update job and reload window
                        putJob(jobId, editjobTitle.value, base64str, editjobDate.value, editjobDesc.value);
                        location.reload();
                    }
                });
            } else { //if no image was posted, update with job's current image. 
                if (validStatus == true) {
                    putJob(jobId, editjobTitle.value, img, editjobDate.value, editjobDesc.value);
                    location.reload();
                }
            }
        })
    })


    //Delete button to delete jobs
    jobPostEditButton.addEventListener("click", function (event) {
        document.getElementById("deletbtn").addEventListener("click", function (event) {
            event.preventDefault();
            deleteJob(jobId);
            location.reload();
        })
    })



    var jobPostDiv5 = document.createElement("div");
    jobPostDiv5.setAttribute("class", "mt-3");

    var jobPostDiv6 = document.createElement("div");

    var jobPostRole = document.createElement("h3");
    jobPostRole.innerText = role;

    var jobPostStartDate = document.createElement("h4");
    jobPostStartDate.innerText = startDate;

    var jobPostAbout = document.createElement("p");
    jobPostAbout.innerText = about;

    var jobPostDiv7 = document.createElement("div");
    jobPostDiv7.setAttribute("class", "text-center")

    var jobPostImg = document.createElement("img");
    jobPostImg.setAttribute("class", "img-fluid w-100");
    jobPostImg.src = img;
    jobPostImg.alt = "job_post_image";

    var jobPostDiv8 = document.createElement("div");
    jobPostDiv8.setAttribute("class", "mt-3 position-relative");

    var jobPostLikesInfoButton = document.createElement("button");
    jobPostLikesInfoButton.setAttribute("class", "text-dark btn btn-link text-decoration-none mb-3 p-0 text-right");
    jobPostLikesInfoButton.setAttribute("data-bs-toggle", "modal");
    jobPostLikesInfoButton.setAttribute("data-bs-target", "#exampleModal");
    jobPostLikesInfoButton.setAttribute("id", `like-modal-btn-${jobId}`);


    var numberOfLikes = document.createElement("span");

    //initial rendering of likes
    if (likes.length == 0) {
        numberOfLikes.innerText = "";
    } else {
        var str = ` Liked by ${likes[0].userName}`;
        if (likes.length > 1) {
            str = str + ` and ${likes.length - 1} other(s)`
        }
        numberOfLikes.innerText = str;
    }
    console.log(likes);

    var jobPostLikesIcon = document.createElement("img");
    jobPostLikesIcon.setAttribute("class", "ms-1");
    jobPostLikesIcon.src = "../img/like_icon.png";
    jobPostLikesIcon.alt = "likes_icon";
    jobPostLikesIcon.setAttribute("height", "18");
    jobPostLikesIcon.setAttribute("width", "20");

    //When likes info is clicked, then renders a modal showing who liked the post
    jobPostLikesInfoButton.addEventListener("click", () => {
        console.log("likes");
        console.log(likes);
        renderListModal("likes", likes)
    }

    );

    var jobPostDiv9 = document.createElement("div");
    jobPostDiv9.setAttribute("class", "d-grid mb-2");

    //Renders the like button
    if (state == "home") {
        var jobPostLikeButton = document.createElement("button");
        jobPostLikeButton.type = "button";
        jobPostLikeButton.setAttribute("class", "btn btn-light btn-block");

        if (hasLiked(index, i) == true) {
            jobPostLikeButton.innerText = "Unlike";
        }
        else {
            jobPostLikeButton.innerText = "Like";
        }
        //Add listener to like button
        jobPostLikeButton.addEventListener("click", function (event) {
            event.preventDefault();
            // check if logged in user has liked comment
            var likeState = !hasLiked(index, i);
            likeJob(jobId, likeState).then(data => {
                if (data["error"] == undefined) {
                    var jobFeed = JSON.parse(localStorage.getItem(`jobFeed-${index}`));
                    var likes = jobFeed[i].likes;
                    if (likeState == true) {
                        jobPostLikeButton.innerText = "Unlike";
                    }
                    else {
                        jobPostLikeButton.innerText = "Like";
                    }
                }
                else {
                    renderError(data["error"])
                }
            })
        });
    }



    var jobPostDiv10 = document.createElement("div");
    jobPostDiv10.setAttribute("class", "accordion mt-3");

    var jobPostDiv11 = document.createElement("div");
    jobPostDiv11.setAttribute("class", "accordion-item border-0");

    var jobPostCommentHeader = document.createElement("h2");
    jobPostCommentHeader.setAttribute("class", "accordion-header");
    jobPostCommentHeader.id = `headingTwo-${jobId}`;

    var jobPostDiv12 = document.createElement("div");
    jobPostDiv12.setAttribute("class", "accordion-button collapsed pointer d-flex justify-content-end");
    jobPostDiv12.setAttribute("data-bs-toggle", "collapse");
    jobPostDiv12.setAttribute("data-bs-target", `#collapseJob1-${jobId}`);
    jobPostDiv12.setAttribute("aria-expanded", "false");
    jobPostDiv12.setAttribute("aria-controls", `collapseJob1-${jobId}`);

    var jobPostCommentCnt = document.createElement("p");
    jobPostCommentCnt.setAttribute("class", "m-0");
    jobPostCommentCnt.setAttribute("id", `num-job-${jobId}`);
    jobPostCommentCnt.innerText = `${comments.length} Comments`;


    var jobPostCommentDiv = document.createElement("div");
    jobPostCommentDiv.setAttribute("class", "accordion-collapse collapse");
    jobPostCommentDiv.setAttribute("data-bs-parent", `#accordionExample-${jobId}`);
    jobPostCommentDiv.setAttribute("aria-labelledby", `headingTwo-${jobId}`);
    jobPostCommentDiv.setAttribute("id", `collapseJob1-${jobId}`);

    var hr1 = document.createElement("hr");
    hr1.setAttribute("class", "m-2");
    var hr2 = document.createElement("hr");
    hr2.setAttribute("class", "m-2");
    var hr3 = document.createElement("hr");

    var jobPostCommentBody = document.createElement("div");
    jobPostCommentBody.setAttribute("class", "accordion-body");
    jobPostCommentBody.setAttribute("id", `commentBody-${jobId}`);

    // comment form
    var commentForm = document.createElement("form");
    commentForm.setAttribute("class", "d-flex my-1");

    var jobPostDiv15 = document.createElement("div");

    var commentUserImg = document.createElement("img");
    commentUserImg.setAttribute("class", "rounded-circle me-3");

    //Gets the image of the current user to display next to comment input box
    getUser(localStorage.getItem("currentUser")).then(data => {
        commentUserImg.src = data.image;
    })

    commentUserImg.alt = "avatar";
    commentUserImg.style = "width: 38px; height: 38px; object-fit: cover;"

    var commentInput = document.createElement("input");
    commentInput.setAttribute("class", "form-control border-0 rounded-pill bg-gray");
    commentInput.setAttribute("id", `send-comment-${jobId}`);
    commentInput.placeholder = "What's on your mind?";
    commentInput.type = "text";
    var commentStr = "";
    //To post comment on job
    commentInput.addEventListener("keypress", function (event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            commentStr = document.getElementById(`send-comment-${jobId}`).value;
            if (commentStr != "")
                commentJob(jobId, commentStr);
            document.getElementById(`send-comment-${jobId}`).value = "";
        }
    });

    // piece everything together by appending
    if (state == "profile") {
        document.getElementById("user-jobs").appendChild(jobPostContainer);
    } else {
        document.getElementById("main").appendChild(jobPostContainer);
    }

    jobPostContainer.appendChild(jobPostDiv1);
    jobPostDiv1.appendChild(jobPostDiv2);
    jobPostDiv2.appendChild(jobPostDiv3);
    jobPostDiv1.appendChild(hr3);
    jobPostDiv3.appendChild(jobPostProfileImg);
    jobPostDiv3.appendChild(jobPostDiv4);

    //append the edit button only if the post was created by current user
    getUser(localStorage.getItem("currentUser")).then(data => {
        if (creatorId == data.id) {
            jobPostDiv2.appendChild(jobPostEditDiv);
            jobPostEditDiv.appendChild(jobPostEditButton);
        }
    });

    jobPostDiv4.appendChild(jobPostName);
    jobPostDiv4.appendChild(jobPostTime);

    jobPostDiv1.appendChild(jobPostDiv5);
    jobPostDiv5.appendChild(jobPostDiv6);
    jobPostDiv6.appendChild(jobPostRole);
    jobPostDiv6.appendChild(jobPostStartDate);
    jobPostDiv6.appendChild(jobPostAbout);
    jobPostDiv6.appendChild(jobPostDiv7);

    jobPostDiv7.appendChild(jobPostImg);

    jobPostDiv6.appendChild(jobPostDiv8);
    jobPostDiv8.appendChild(jobPostLikesInfoButton);
    jobPostLikesInfoButton.appendChild(jobPostLikesIcon);
    jobPostLikesInfoButton.appendChild(numberOfLikes);

    jobPostDiv8.appendChild(jobPostDiv9);
    if (state == "home") {
        jobPostDiv9.appendChild(jobPostLikeButton);
    }

    jobPostDiv8.appendChild(jobPostDiv10);
    jobPostDiv8.appendChild(jobPostDiv11);

    jobPostDiv11.appendChild(jobPostCommentHeader);
    jobPostCommentHeader.appendChild(jobPostDiv12);
    jobPostDiv12.appendChild(jobPostCommentCnt);

    jobPostDiv11.appendChild(jobPostCommentDiv);
    jobPostCommentDiv.appendChild(jobPostCommentBody);

    //Generates the comments on the post
    for (let i = 0; i < comments.length; i++) {
        getUser(comments[i].userId).then(data => {
            const img = data.image;
            generateComment(
                `commentBody-${jobId}`,
                comments[i].userName,
                comments[i].comment,
                img,
                comments[i].userId,
            )
        }).catch(error => {//If we are not connected to the backend, instead genearte comments without user's image
            generateComment(
                `commentBody-${jobId}`,
                comments[i].userName,
                comments[i].comment,
                "",
                comments[i].userId,
            )
        })
    }

    jobPostCommentBody.appendChild(commentForm);
    commentForm.appendChild(jobPostDiv15);
    jobPostDiv15.appendChild(commentUserImg);
    commentForm.appendChild(commentInput);
}

//function to check if the post is liked by the current user
function hasLiked(idx, i) {
    //returns false if post has not been like and true otherwise
    var jobFeed = JSON.parse(localStorage.getItem(`jobFeed-${idx}`));
    var likes = jobFeed[i].likes;
    var likeState = false;
    for (let j = 0; j < likes.length; j++) {
        if (likes[j].userId == localStorage.getItem("currentUser")) {
            likeState = true;
        }
    }
    return likeState;

}

//function to generate comments on a post
function generateComment(id, name, comment, img, userId) {
    var commentDiv1 = document.createElement("div");
    commentDiv1.setAttribute("class", "d-flex align-items-center my-1");
    commentDiv1.addEventListener("click", function (event) {
        event.preventDefault();
        changeHash(`#me=${userId}`)
    })
    var commentImg = document.createElement("img");
    commentImg.setAttribute("class", "rounded-circle me-2")
    commentImg.src = img;
    commentImg.alt = "comment_profile_pic";
    commentImg.style = "width: 38px; height: 38px; object-fit: cover;";

    var commentDiv2 = document.createElement("div");
    commentDiv2.setAttribute("class", "p-3 rounded w-100");


    var commentName = document.createElement("p");
    commentName.setAttribute("class", "btn fw-bold m-0 p-0");
    commentName.innerText = name;

    var commentText = document.createElement("p");
    commentText.setAttribute("class", "m-0 fs-7 bg-gray p-2 rounded");
    commentText.innerText = comment;

    commentDiv1.appendChild(commentImg);
    commentDiv1.appendChild(commentDiv2);
    commentDiv2.appendChild(commentName);
    commentDiv2.appendChild(commentText);

    let commentBody = document.getElementById(id);
    let lastChild = commentBody.lastChild;
    commentBody.insertBefore(commentDiv1, lastChild);
}

export function update5post() {
    //gets the jobIDs from getFeed index = 0
    getFeed(0).then(data => {
        if (data['error'] == undefined && data.length > 0) {
            for (let i = 0; i < data.length; i++) {
                var commentContainer = document.querySelector(`#commentBody-${data[i].id}`);
                var commentCurrent;
                var num = document.getElementById(`num-job-${data[i].id}`);
                num.innerText = `${data[i].comments.length} Comments`;
                if (num.innerText == null) {
                    return;
                }
                if (commentContainer != null) {
                    commentCurrent = commentContainer.querySelectorAll("div.align-items-center");
                    //if the database has more comments than what has been rendered
                    //then generate the new comments from data
                    if (commentCurrent.length < data[i].comments.length) {
                        for (let j = commentCurrent.length; j < data[i].comments.length; j++) {
                            getUser(data[i].comments[j].userId).then(data2 => {
                                const img = data2.image;
                                generateComment(
                                    `commentBody-${data[i].id}`,
                                    data[i].comments[j].userName,
                                    data[i].comments[j].comment,
                                    img,
                                    data[i].comments[j].userId,
                                )
                            })
                        }
                    }
                }
                //Check if the user has liked and update the like button
                if (document.querySelector(`#post-${data[i].id} button.btn-block`) == null) {
                    return;
                }
                if (hasLiked(0, i)) {
                    document.querySelector(`#post-${data[i].id} button.btn-block`).innerText = "Unlike"
                }
                else {
                    document.querySelector(`#post-${data[i].id} button.btn-block`).innerText = "Like"
                }

                var numberOfLikes = document.querySelector(`#post-${data[i].id} button span`);
                //update the number of likes string
                if (data[i].likes.length == 0) {
                    numberOfLikes.innerText = "";
                } else {
                    var str = ` Liked by ${data[i].likes[0].userName}`;
                    if (data[i].likes.length > 1) {
                        str = str + ` and ${data[i].likes.length - 1} other(s)`;
                    }
                    numberOfLikes.innerText = str;
                }

            }


            localStorage.setItem("lock", false);
        }

    });

}
