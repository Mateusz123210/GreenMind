import { useLocalStorage } from "@/hooks/useLocalStorage";
import { guardResOk, logout, refreshTokens } from "./auth";
import useSWR from "swr";

export const fetchBackend = async (input: string | URL, init?: RequestInit, additionalQuery?: Record<string, string>): Promise<Response> => {
    const url = (input instanceof URL) ? input : new URL(window.location.origin + input);
    const at = localStorage.getItem("access_token");
    const email = localStorage.getItem("email");
    url.searchParams.append("accessToken", at!);
    url.searchParams.append("access_token", at!);
    url.searchParams.append("email", email!);
    if (additionalQuery) { 
        Object.entries(additionalQuery).forEach(([key, val]) => {
            url.searchParams.append(key, val)
        })
    }
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
    "Content-Type": "application/json",
};

export const postBackend = (input: string, body: object): Promise<Response> => {
    return fetchBackend(input, {
        method: "POST",
        headers: headersJsonContentType,
        body: JSON.stringify(body),
    });
};

export const putBackend = (input: string, body: object): Promise<Response> => {
    return fetchBackend(input, {
        method: "PUT",
        headers: headersJsonContentType,
        body: JSON.stringify(body),
    });
};

export const deleteBackend = (input: string | URL): Promise<Response> => {
    return fetchBackend(input, {
        method: "DELETE",
    });
};

export const jsonFetcher = (...args: Parameters<typeof fetchBackend>) =>
    fetchBackend(...args).then((res) => res.json()).then(data => {
        console.log(data)
        return data
    });

export const useLoginInfo = () => useLocalStorage("email");

export const useBackend = <T>(url: string, additionalQuery?: Record<string, string>) => {
    const isLoggedIn = Boolean(useLoginInfo());
    return useSWR<T>(isLoggedIn && [url, ...(!additionalQuery ? [] : Object.keys(additionalQuery))], ([url]) => jsonFetcher(url, undefined, additionalQuery))
}
