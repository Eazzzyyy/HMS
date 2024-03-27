
    document.getElementById("changePass").addEventListener("click", (() => {
        window.location.href = `/forgot-password?type=change&username=${document.getElementById('usernamehidden').textContent}`
    }));

    document.getElementById('editBtn').addEventListener('click', function () {
        document.getElementById("email").disabled = true;
        document.querySelectorAll('.form-control').forEach(function (input) {
            input.removeAttribute('readonly');
        });

        document.getElementById('editBtn').style.display = 'none';
        document.getElementById('changePass').style.display = 'none';

        document.getElementById('saveBtn').classList.remove('d-none');
        document.getElementById('cancelBtn').classList.remove('d-none');
    });

    document.getElementById('cancelBtn').addEventListener('click', function () {
        document.getElementById('editBtn').style.display = 'block';
        document.getElementById('changePass').style.display = 'block';
        document.getElementById("email").disabled = false;
        document.querySelectorAll('#editProfileForm input').forEach(function (input) {
            input.setAttribute('readonly', true);
        });

        document.getElementById('editBtn').classList.remove('d-none');
        document.getElementById('saveBtn').classList.add('d-none');
        document.getElementById('cancelBtn').classList.add('d-none');
    });

    document.getElementById("saveBtn").addEventListener("click", () => {
        const firstName = document.getElementById("fname").value;
        const lastName = document.getElementById("lname").value;
        const email = document.getElementById("email").value;
        const contact = document.getElementById("contact").value;

        const data = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            contact_number: contact
        };

        fetch('/profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                console.error('Error updating profile');
            }
        })
        .then(jsonResponse => {
            console.log(jsonResponse);
            if (jsonResponse.contact) {
                document.getElementById("errored").innerHTML = jsonResponse.contact;
            } else {
                document.getElementById("errored").innerHTML = "";

                const successMessage = document.createElement('div');
                successMessage.classList.add('messages', 'alert', 'alert-dismissible', 'alert-success');
                successMessage.setAttribute('role', 'alert');
                successMessage.innerHTML = `
                    <div>
                        ${jsonResponse.success}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                `;
                document.getElementById("aler_message").appendChild(successMessage);

                setTimeout(() => {
                    window.location.href = '/profile/';
                }, 1500);
            }
        })
        .catch(error => {
            console.error('Error updating profile:', error);
        });
    });

