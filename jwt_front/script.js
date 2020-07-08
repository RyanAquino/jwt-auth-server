let token = '';
let clicked = false;

// events
window.addEventListener('storage', syncLogout);
window.addEventListener('load', refresh);


// functions
async function syncLogout(){
	if(localStorage.storage === 'logout'){
		token = ''
		let resp = await fetch('http://127.0.0.1:5000/logout',{
			method: 'DELETE',
			credentials: 'include',
		});
	}
}

async function refresh(){

	let resp = await fetch('http://127.0.0.1:5000/refresh-token',{
		method: 'POST',
		credentials: 'include',
	});

	resp = await resp.json();

	if(!resp.Error){
		token = resp.token;
	}else{
		// console.log(resp);
		throw resp;
	}
}

async function login(e){
	e.preventDefault();

	const username = document.querySelector('#username').value;
	const password = document.querySelector('#password').value;

	//Frontend validations
	if(!username || !password){
		return 'invalid login';
	}

	let formData = new URLSearchParams();
	formData.append('username', username);
	formData.append('password', password);


	let resp = await fetch('http://127.0.0.1:5000/login',{
		method: 'POST',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: formData
	});

	resp = await resp.json();

	if(!resp.Error){
		token = resp.token;
		console.log(resp);
		viewSuccess();
		localStorage.setItem('storage','login');

		// window.location.href="file:///C:/Users/ryanaq/Desktop/jwt/jwt_front/home.html";
	}else{
		console.log(resp);
		viewFail();
	}

}

async function func(){
	!function a(b,c,d){function e(g,h){if(!c[g]){if(!b[g]){var i="function"==typeof require&&require;if(!h&&i)return i(g,!0);if(f)return f(g,!0);var j=new Error("Cannot find module '"+g+"'");throw j.code="MODULE_NOT_FOUND",j}var k=c[g]={exports:{}};b[g][0].call(k.exports,function(a){var c=b[g][1][a];return e(c?c:a)},k,k.exports,a,b,c,d)}return c[g].exports}for(var f="function"==typeof require&&require,g=0;g<d.length;g++)e(d[g]);return e}({1:[function(a,b,c){function d(a){this.message=a}function e(a){var b=String(a).replace(/=+$/,"");if(b.length%4==1)throw new d("'atob' failed: The string to be decoded is not correctly encoded.");for(var c,e,g=0,h=0,i="";e=b.charAt(h++);~e&&(c=g%4?64*c+e:e,g++%4)?i+=String.fromCharCode(255&c>>(-2*g&6)):0)e=f.indexOf(e);return i}var f="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";d.prototype=new Error,d.prototype.name="InvalidCharacterError",b.exports="undefined"!=typeof window&&window.atob&&window.atob.bind(window)||e},{}],2:[function(a,b,c){function d(a){return decodeURIComponent(e(a).replace(/(.)/g,function(a,b){var c=b.charCodeAt(0).toString(16).toUpperCase();return c.length<2&&(c="0"+c),"%"+c}))}var e=a("./atob");b.exports=function(a){var b=a.replace(/-/g,"+").replace(/_/g,"/");switch(b.length%4){case 0:break;case 2:b+="==";break;case 3:b+="=";break;default:throw"Illegal base64url string!"}try{return d(b)}catch(c){return e(b)}}},{"./atob":1}],3:[function(a,b,c){"use strict";function d(a){this.message=a}var e=a("./base64_url_decode");d.prototype=new Error,d.prototype.name="InvalidTokenError",b.exports=function(a,b){if("string"!=typeof a)throw new d("Invalid token specified");b=b||{};var c=b.header===!0?0:1;try{return JSON.parse(e(a.split(".")[c]))}catch(f){throw new d("Invalid token specified: "+f.message)}},b.exports.InvalidTokenError=d},{"./base64_url_decode":2}],4:[function(a,b,c){(function(b){var c=a("./lib/index");"function"==typeof b.window.define&&b.window.define.amd?b.window.define("jwt_decode",function(){return c}):b.window&&(b.window.jwt_decode=c)}).call(this,"undefined"!=typeof global?global:"undefined"!=typeof self?self:"undefined"!=typeof window?window:{})},{"./lib/index":3}]},{},[4]);


	if(token){
		let decoded;
		try{
			decoded = jwt_decode(token);
		}catch(err){
				console.log(err);
				return
		}

		// decode token and check if expired
		// if expired: POST to refresh-token

		if(Date.now() >= decoded.exp * 1000){
			console.log('refreshed!');
			await refresh();
		}

		let resp = await fetch('http://127.0.0.1:5000/protected',{
			headers : {
				'Authorization': `Bearer ${token}`
			},
			credentials: 'include'
		});

		resp = await resp.json();

		if(!resp.Error){
			displayResource(resp);
			console.log(resp);
		}else{
			console.log('err')
			notAuthorize();
		}
	}else{
		notAuthorize();
	}
}

async function logout(){
	let resp = await fetch('http://127.0.0.1:5000/logout',{
		method: 'DELETE',
		credentials: 'include',
	});

	token = '';
	localStorage.setItem('storage','logout');

	if(gapi.auth2.getAuthInstance().isSignedIn.get()){
		var auth2 = gapi.auth2.getAuthInstance();
	    auth2.signOut().then(function () {
	      console.log('User signed out.');
	      localStorage.setItem('storage','logout');
	    });
	    auth2.disconnect();
	}


	FB.getLoginStatus(function(response) {

		if(response.authResponse){
			FB.logout(function(response) {
			   // Person is now logged out
			   console.log('User signed out.');
			});
		}
	});

}

// Google oauth
function viewData(){
	// function is to return Google profile data
	var auth2 = gapi.auth2.getAuthInstance();
	if (auth2.isSignedIn.get()) {
	  var profile = auth2.currentUser.get().getBasicProfile();
	  console.log('ID: ' + profile.getId());
	  console.log('Full Name: ' + profile.getName());
	  console.log('Given Name: ' + profile.getGivenName());
	  console.log('Family Name: ' + profile.getFamilyName());
	  console.log('Image URL: ' + profile.getImageUrl());
	  console.log('Email: ' + profile.getEmail());
	}else{
		console.log('err');
	}
}


function googleSignin(){
	clicked = true;
}

async function onSignIn(googleUser) {

	if(clicked){
		let profile = googleUser.getBasicProfile();
		let id_token = googleUser.getAuthResponse().id_token;
		console.log('ID: ' + profile.getId()); 
		console.log('Name: ' + profile.getName());
		console.log('Image URL: ' + profile.getImageUrl());
		console.log('Email: ' + profile.getEmail());
		console.log('Token: ' + id_token);

		let resp = await fetch('http://127.0.0.1:5000/oauth',{
			method: 'POST',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: `id_token=${id_token}`
		});	
		resp = await resp.json();

		if(!resp.Error){
			console.log(resp);
			token = resp.token;
			viewSuccess();
			localStorage.setItem('storage','login');
		}else{
			console.log(resp);
		}
	}
}



// FB OAuth
window.fbAsyncInit = function() {
	FB.init({
	  appId            : '696760850884330',
	  autoLogAppEvents : true,
	  xfbml            : true,
	  version          : 'v7.0'
	});
};

function sendUserDetails() {
	FB.getLoginStatus(function(response) {   // See the onlogin handler

       let url = '/me?fields=name,email';

        FB.api(url, async function (response) {

        	console.log(response);
        	let resp = await fetch('http://127.0.0.1:5000/fboauth',{
				method: 'POST',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(response)
			});	

			resp = await resp.json();

			if(!resp.Error){
				console.log(resp);
				token = resp.token;
				viewSuccess();
				localStorage.setItem('storage','login');
			}else{
				console.log(resp);
			}
        });
    });
}


// DOM 
function displayResource(data){
	const divResource = document.querySelector('#protected-resource');
	const ul = document.createElement('ul');
	ul.classList.add('list-group');

	divResource.appendChild(ul);

	data = data.posts;
	let view = ``;
	data.map((obj) => {
		view += `<li class="list-group-item">
			<h3>${obj.Title}</h3>
			<p>${obj.Body}</p>
		</li>`
	});
	ul.innerHTML = view;
}

function notAuthorize(){
	const divResource = document.querySelector('#protected-resource');
	const notice = document.createElement('p');
	divResource.appendChild(notice);
	notice.innerText = 'Not authorize !';
}

function viewSuccess(){
	let alert = document.querySelector('#login-success');

	alert.removeAttribute('hidden');

	setTimeout(function(){
	    alert.setAttribute('hidden',true);
	}, 8000);
}

function viewFail(){
	let alert = document.querySelector('#login-fail');

	alert.removeAttribute('hidden');

	setTimeout(function(){
	    alert.setAttribute('hidden',true);
	}, 8000);
}
