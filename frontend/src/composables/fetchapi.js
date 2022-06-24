// const headers = { "Content-Type": "application/json;charset=utf-8", "X-Requested-With": "XMLHttpRequest" }
// const get_data = async (url) => await fetch(url, { method: "GET", headers })
// const save_data = async (url, body, csrf) => await fetch(url, { method: "POST", headers: { ...headers, "X-CSRFToken": csrf }, body: JSON.stringify(body) })

export default {
    headers: { "Content-Type": "application/json;charset=utf-8", "X-Requested-With": "XMLHttpRequest" },
    async get_data(url) {
        return await fetch(
            url, { method: "GET", headers: this.headers }
        )
    },
    async save_data(url, body, csrf) {
        return await fetch(
            url, { method: "POST", headers: { ...this.headers, "X-CSRFToken": csrf }, body: JSON.stringify(body) }
        )
    }
}
