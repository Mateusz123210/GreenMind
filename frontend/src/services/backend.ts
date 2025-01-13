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
