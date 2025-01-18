import { useLocalStorage } from "@/hooks/useLocalStorage";
import { guardResOk, logout, refreshTokens } from "./auth";
import useSWR from "swr";
import { useEffect, useMemo, useState } from "react";
import { enqueueSnackbar } from "notistack";

export const fetchBackend = async (
    input: string | URL,
    init?: RequestInit,
    additionalQuery?: Record<string, string>
): Promise<Response> => {
    var url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}` + input);
    var at = localStorage.getItem("access_token");
    var email = localStorage.getItem("email");
    url.searchParams.append("accessToken", at!);
    url.searchParams.append("access_token", at!);
    url.searchParams.append("email", email!);
    if (additionalQuery) {
        Object.entries(additionalQuery).forEach(([key, val]) => {
            url.searchParams.append(key, val);
        });
    }
    var response = await fetch(url, init);
    if (response.status == 401) {

        const refreshTokenResponse = await refreshTokens();
        url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}` + input);
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

export const useSSE = <T>(path: string, additionalQuery?: Record<string, string>) => {
    const email = useLoginInfo();
    const eventSource = useMemo(() => {
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
        return new EventSource(url);
    }, [email, additionalQuery, path]);
    
    const [currentValue, setCurrentValue] = useState<T | null>(null);
    useEffect(() => {
        eventSource.onerror = (er) => {
            console.log(er)
            enqueueSnackbar(String(er), {variant: "error"})
        }
        eventSource.onmessage = (ev) => {
           setCurrentValue(ev.data); 
        }
        return () => {
            eventSource.close()
        }
    }, [eventSource]);
    return currentValue;
};
