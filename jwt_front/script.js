let token = '';

window.addEventListener('storage', syncLogout);

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

refresh();

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
		localStorage.setItem('storage','login');
		// window.location.href="file:///C:/Users/ryanaq/Desktop/jwt/jwt_front/home.html";
	}else{
		console.log(resp);
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
			console.log(resp);
		}else{
			console.log('err')
		}
	}
}

async function logout(){
	let resp = await fetch('http://127.0.0.1:5000/logout',{
		method: 'DELETE',
		credentials: 'include',
	});
	token = '';
	localStorage.setItem('storage','logout');
}