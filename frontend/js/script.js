
const form = document.getElementById("shorten-form");
const input = document.getElementById("long-link");
const button = document.getElementById("submit-button");

const result = document.getElementById("result");
const shortLink = document.getElementById("short-link");
const copyButton = document.getElementById("copy-button");

const message = document.getElementById("message");

function showMessage(text, type = "error") {
    message.textContent = text;
    message.className = `message ${type}`;
}

function clearMessage() {
    message.textContent = "";
    message.className = "message";
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const longLink = input.value.trim();

    result.style.display = "none";
    clearMessage();

    button.disabled = true;
    button.textContent = "Encurtando...";

    try {
        const response = await fetch("/link/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                long_link: longLink
            })
        });

        const data = await response.json();

        if (response.status === 429) {
            showMessage(
                "Você atingiu o limite de requisições. Aguarde um pouco antes de tentar novamente.",
                "warning"
            );
            return;
        }

        if (!response.ok) {
            showMessage(
                data.detail || "Não foi possível encurtar seu link.",
                "error"
            );
            return;
        }

        if (!data.short_link) {
            throw new Error("A API não retornou o link encurtado.");
        }

        shortLink.href = data.short_link;
        shortLink.textContent = data.short_link;

        result.style.display = "block";

        showMessage(
            "Link encurtado com sucesso! Agora você pode copiar e compartilhar.",
            "success"
        );

    } catch (error) {
        showMessage(
            error instanceof TypeError
                ? "Não conseguimos conectar ao servidor. Tente novamente mais tarde."
                : error.message,
            "error"
        );

    } finally {
        button.disabled = false;
        button.textContent = "Encurtar";
    }
});

copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(shortLink.href);

        copyButton.textContent = "Copiado!";

        showMessage(
            "Link copiado para a área de transferência!",
            "success"
        );

        setTimeout(() => {
            copyButton.textContent = "Copiar";
        }, 2000);

    } catch {
        showMessage(
            "Não foi possível copiar automaticamente. Copie o link manualmente.",
            "error"
        );
    }
});
