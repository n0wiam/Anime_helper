let currentPage = 1;

async function searchAnime(page = 1) {
    const keyword = document.getElementById("keyword").value.trim();
    if (!keyword) {
        alert("请输入动漫名称");
        return;
    }

    currentPage = page;

    const res = await fetch("/anime/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: keyword,
            number: page
        })
    });

    const json = await res.json();
    renderAnimeList(json.data);
}

function renderAnimeList(animes) {
    const list = document.getElementById("anime-list");
    list.innerHTML = "";

    if (!animes || animes.length === 0) {
        list.innerHTML = "<p>没有搜索到结果</p>";
        return;
    }

    animes.forEach(anime => {
        const div = document.createElement("div");
        div.className = "anime-card";

        div.innerHTML = `
            <img src="${anime.image_url}" alt="${anime.name}">
            <div class="anime-name">${anime.name}</div>
        `;

        div.querySelector("img").onclick = () => showDetail(anime);
        list.appendChild(div);
    });
}

/* 详情弹窗 */
function showDetail(anime) {
    document.getElementById("m-name").innerText = anime.name;
    document.getElementById("m-status").innerText = anime.status;
    document.getElementById("m-total").innerText = anime.total_number;
    document.getElementById("m-info").innerText = anime.info;

    document.getElementById("modal").style.display = "flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

// 订阅动漫
window.openSubModal = function () {
    document.getElementById("sub-modal").style.display = "flex";
};

window.closeSubModal = function () {
    document.getElementById("sub-modal").style.display = "none";
};

window.submitSubscribe = function () {
    const watch = document.getElementById("sub-watch").value;
    const link = document.getElementById("sub-link").value.trim();

    if (!watch || !link) {
        alert("请填写完整信息");
        return;
    }

    fetch("/anime/sub", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            anime_id: currentAnimeId,
            watch_number: Number(watch),
            user_link: link
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("订阅成功 🎉");
            closeSubModal();
        } else {
            alert(data.msg || "订阅失败");
        }
    })
    .catch(() => alert("网络异常"));
};