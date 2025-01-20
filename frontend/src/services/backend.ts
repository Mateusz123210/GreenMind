import { useLocalStorage } from "@/hooks/useLocalStorage";
import { guardResOk, refreshTokens, updateStorage } from "./auth";
import useSWR from "swr";
import { useEffect, useMemo, useState } from "react";
import { enqueueSnackbar } from "notistack";
import { SensorUpdate } from "@/types/rest";

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
    let response = await fetch(url, init);
    if (response.status == 401) {
        const refreshTokenResponse = await refreshTokens(at!);
        if (refreshTokenResponse !== null){

            url = new URL(process.env.NEXT_PUBLIC_BACKEND_URL! + input);
            url.searchParams.append("accessToken", refreshTokenResponse!["access_token"]);
            url.searchParams.append("access_token", refreshTokenResponse!["access_token"]);
            url.searchParams.append("email", email!);

            updateStorage("access_token", refreshTokenResponse!["access_token"]);
            updateStorage("refresh_token", refreshTokenResponse!["refresh_token"]);

            response = await fetch(url, init);
            if (response.status == 403) {
                localStorage.clear();
                window.dispatchEvent(new Event("storage"));
                return guardResOk(response);
            }
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

export const postBackend = (
    input: string,
    body: object,
    additionalQuery?: Record<string, string>
): Promise<Response> => {
    return fetchBackend(
        input,
        {
            method: "POST",
            headers: headersJsonContentType,
            body: JSON.stringify(body),
        },
        additionalQuery
    );
};

export const putBackend = (
    input: string,
    body: object,
    additionalQuery?: Record<string, string>
): Promise<Response> => {
    return fetchBackend(
        input,
        {
            method: "PUT",
            headers: headersJsonContentType,
            body: JSON.stringify(body),
        },
        additionalQuery
    );
};

export const deleteBackend = (
    input: string | URL,
    additionalQuery?: Record<string, string>
): Promise<Response> => {
    return fetchBackend(
        input,
        {
            method: "DELETE",
        },
        additionalQuery
    );
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
            let dederangedData = JSON.parse(ev.data);
            if ("message" in dederangedData) {
                dederangedData = null;
            }
            setCurrentValue(dederangedData);
        };
        return () => {
            eventSource.close();
        };
    }, [additionalQuery, email, path]);
    if (currentValue) console.log(`currentValue ${currentValue}`);
    return currentValue;
};

export function mapValue(
    value: number,
    oldMin: number,
    oldMax: number,
    newMin: number,
    newMax: number
) {
    const mapped = ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
    return Math.max(3, mapped);
}

export const useSensorUpdate = (plantationid: string) => {
    const plantationQueryParams = useMemo(() => ({plantationUUID: plantationid}), [plantationid])
    const [wilg, temp, nasl, timestamp] =
        useSSE<SensorUpdate>("/api/sensors", plantationQueryParams) ?? [];
    const date = timestamp && new Date(timestamp * 1000);
    const parsedWilg = wilg && mapValue(wilg, 300, 1000, 0, 100);
    return parsedWilg && temp && nasl && date ? ([parsedWilg, temp, nasl, date] as const) : null;
};
