/**@type {HTMLInputElement} */
const $token = document.querySelector("input[name='token']");
/**@type {HTMLInputElement} */
const $pass = document.querySelector("input[name='password']");
/**@type {HTMLInputElement} */
const $pass_copy = document.querySelector("input[name='password-copy']");
/**@type {HTMLButtonElement} */
const $submit = document.getElementById("submit");

/**@type {HTMLElement} */
const $error_message = document.getElementById("error_message");

window["change_password"] = function (/**@type {PointerEvent} */ { target }) {
	if (!$pass) return;
	[$pass.type, target.textContent] =
		$pass.type === "password" ? ["text", "hide"] : ["password", "show"];
};

window["change_password_copy"] = function (
	/**@type {PointerEvent} */ { target }
) {
	if (!$pass_copy) return;
	[$pass_copy.type, target.textContent] =
		$pass_copy.type === "password" ? ["text", "hide"] : ["password", "show"];
};

document.addEventListener("submit", async (e) => {
	e.preventDefault();
	if (!$pass || !$pass_copy || !$token) return;
	const samePass = $pass.value === $pass_copy.value;
	console.log(samePass);
	if (!samePass) {
		$error_message.textContent = "ambas contraseñas deben ser iguales";
		return $pass_copy.classList.add("error");
	} else $pass_copy.classList.remove("error");
	console.log($pass.value);
	console.log($pass_copy.value);

	try {
		$submit.disabled = true;
		const res = await fetch(e.target.action, {
			method: "PATCH",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				password: $pass.value,
				token: $token.value,
			}),
		});
		if (res.ok) {
			$submit.textContent = "Contraseña actualizada";
            $submit.classList.add("success")
			$error_message.textContent = "";
            return;
		}
        const data = await res.json().catch((e)=>{
            console.log(e)
            return {}
        });
        console.log(data);
        $submit.disabled = false;
        $error_message.textContent = data?.error || "Error al actualizar";
	} catch (error) {
		console.log(error);
		$error_message.textContent =
			"ocurrio un error inesperado, intentelo más tarde";
		$submit.disabled = false;
	}
});
