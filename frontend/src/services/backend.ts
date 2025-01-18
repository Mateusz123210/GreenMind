import { useLocalStorage } from "@/hooks/useLocalStorage";
import { guardResOk, refreshTokens } from "./auth";
import useSWR from "swr";
import { useEffect, useState } from "react";
import { enqueueSnackbar } from "notistack";

export const fetchBackend = async (
    input: string | URL,
    init?: RequestInit,
    additionalQuery?: Record<string, string>
): Promise<Response> => {
    let url = input instanceof URL ? input : new URL(process.env.NEXT_PUBLIC_BACKEND_URL + input);
    const at = localStorage.getItem("access_token");
    const email = localStorage.getItem("email");
    url.searchParams.append("accessToken", at!);
    url.searchParams.append("access_token", at!);
    url.searchParams.append("email", email!);
    if (additionalQuery) {
        Object.entries(additionalQuery).forEach(([key, val]) => {
            url.searchParams.append(key, val);
        });
    }
    const response = await fetch(url, init);
    if (response.status == 401) {
        const refreshTokenResponse = await refreshTokens();
        url = new URL(process.env.NEXT_PUBLIC_BACKEND_URL! + input);
        url.searchParams.append("accessToken", refreshTokenResponse!["access_token"]);
        url.searchParams.append("access_token", refreshTokenResponse!["access_token"]);
        url.searchParams.append("email", refreshTokenResponse!["email"]);
        const fetchResponse = await fetch(url, init);
        if (fetchResponse.status == 403) {
            localStorage.clear();
            window.dispatchEvent(new Event("storage"));
            return guardResOk(response);
        }
        return guardResOk(response);
    }
    if (response.status == 403) {
        localStorage.clear();
        window.dispatchEvent(new Event("storage"));
        return guardResOk(response);
    }

    return guardResOk(response);
};

export const headersJsonContentType = {
    "Content-Type": "application/json",
};

export const postBackend = (input: string, body: object, additionalQuery?: Record<string, string>): Promise<Response> => {
    return fetchBackend(input, {
        method: "POST",
        headers: headersJsonContentType,
        body: JSON.stringify(body),
    }, additionalQuery);
};

export const putBackend = (input: string, body: object, additionalQuery?: Record<string, string>): Promise<Response> => {
    return fetchBackend(input, {
        method: "PUT",
        headers: headersJsonContentType,
        body: JSON.stringify(body),
    }, additionalQuery);
};

export const deleteBackend = (input: string | URL, additionalQuery?: Record<string, string>): Promise<Response> => {
    return fetchBackend(input, {
        method: "DELETE",
    }, additionalQuery);
};

export const jsonFetcher = (...args: Parameters<typeof fetchBackend>) =>
    fetchBackend(...args)
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            return data;
        });

export const useLoginInfo = () => useLocalStorage("email");

export const useBackend = <T>(url: string, additionalQuery?: Record<string, string>) => {
    const isLoggedIn = Boolean(useLoginInfo());
    return useSWR<T>(
        isLoggedIn && [url, ...(!additionalQuery ? [] : Object.keys(additionalQuery))],
        ([url]) => jsonFetcher(url, undefined, additionalQuery)
    );
};

//wilgotność temp nasł
export const useSSE = <T>(path: string, additionalQuery?: Record<string, string>) => {
    const email = useLoginInfo();

    const [currentValue, setCurrentValue] = useState<T | null>(null);
    useEffect(() => {
        const url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}` + path);
        const at = localStorage.getItem("access_token");
        url.searchParams.append("accessToken", at!);
        url.searchParams.append("access_token", at!);
        url.searchParams.append("email", email!);
        if (additionalQuery) {
            Object.entries(additionalQuery).forEach(([key, val]) => {
                url.searchParams.append(key, val);
            });
        }
        const eventSource = new EventSource(url);

        eventSource.onerror = (er) => {
            console.log(er);
            enqueueSnackbar(String(er), { variant: "error" });
        };
        eventSource.onmessage = (ev) => {
            console.log(`server event data ${ev.data}`);
            setCurrentValue(ev.data);
        };
        return () => {
            eventSource.close();
        };
    }, [additionalQuery, email, path]);
    return currentValue;
};
