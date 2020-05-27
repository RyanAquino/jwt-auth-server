let token = '';

(async function(){

	let resp = await fetch('http://127.0.0.1:5000/refresh-token',{
		method: 'POST',
		credentials: 'include',
	});


	if(resp.ok){
		resp = await resp.json();
		token = resp.token;
	}

})();

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

	console.log(resp.ok);
	if(resp.ok){
		resp = await resp.json();
		token = resp.token;
		console.log(resp);
		window.location.href="file:///C:/Users/ryanaq/Desktop/jwt/jwt_front/home.html";
	}else{
		console.log(resp);
	}

}

async function func(){

	if(token){
		let resp = await fetch('http://127.0.0.1:5000/protected',{
			headers : {
				'Authorization': `Bearer ${token}`
			},
			credentials: 'include'
		});

		if(resp.ok){
			resp = await resp.json();
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
}