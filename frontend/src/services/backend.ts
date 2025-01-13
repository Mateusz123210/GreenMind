import { guardResOk, logout, refreshTokens } from "./auth";

export const fetchBackend = async (input: string | URL, init?: RequestInit): Promise<Response> => {
    const url = new URL(input);
    const at = localStorage.getItem("access_token");
    const email = localStorage.getItem("email");
    url.searchParams.append("access_token", at!);
    url.searchParams.append("email", email!);
    const response = await fetch(url, init);
    if (response.status == 401) {
        await refreshTokens();
        return fetchBackend(input, init);
    }
    if (response.status == 403) {
        logout();
        return response;
    }

    return guardResOk(response);
};

export const headersJsonContentType = {
    "Content-Type": "application/json"
}

export const postBackend = (input: string, body: object): Promise<Response> => {
    return fetchBackend(input, {
        method: "POST",
        headers: headersJsonContentType,
        body: JSON.stringify(body)
    })
}

export const jsonFetcher = (...args: Parameters<typeof fetch>) => fetch(...args).then(res => res.json())