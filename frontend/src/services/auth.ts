import { enqueueSnackbar } from "notistack";
import { headersJsonContentType } from "./backend";
import { Mutex } from "async-mutex";

export interface User {
    email: string;
    accessToken: string;
    refreshToken: string;
}

export const guardResOk = (res: Response) => {
    if (res.ok) {
        return Promise.resolve(res);
    } else {
        res.json().then((json) => enqueueSnackbar(String(json?.detail), { variant: "error" }));
        console.log(res.status);
        console.log(res.statusText);
        return Promise.reject(res.status);
    }
};

export const emailRegex =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'/;

export const isPasswordCorrect = (password: string) => {
    if (password.length < 8) return false;

    if ([...password].filter((x) => [1, 2, 3, 4, 5, 6, 7, 8, 9].includes(Number(x))).length == 0)
        return false;

    if (![...password].some((c) => c == c.toUpperCase())) return false;

    if (![...password].some((c) => c == c.toLowerCase())) return false;

    const regexp = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
    if (!regexp.test(password)) return false;

    return true;
};

export const register = (email: string, password: string) => {
    return fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}api/register`, {
        method: "POST",
        headers: headersJsonContentType,
        body: JSON.stringify({
            email,
            password,
        }),
    }).then(guardResOk);
};

export const login = (email: string, password: string) => {
    return fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/login`, {
        method: "POST",
        headers: headersJsonContentType,
        body: JSON.stringify({
            email,
            password,
        }),
    })
        .then(guardResOk)
        .then((res) => res.json())
        .then((data) => {
            updateStorage("email", email);
            updateStorage("access_token", data.access_token);
            updateStorage("refresh_token", data.refresh_token);
        });
};


const tokens = {"previous_access_token": "", "access_token": "", "refresh_token": ""}
const mutex = new Mutex()

export const refreshTokens = async (prev_access_token: string) => {
    return mutex.runExclusive(async () => {

        if (prev_access_token === tokens["previous_access_token"]){
            return {
                access_token: tokens["access_token"],
                refresh_token: tokens["refresh_token"],
            };

        }

        tokens["previous_access_token"] = prev_access_token

        const url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/refresh-token`);
        url.searchParams.append("refreshToken", localStorage.getItem("refresh_token")!);
        url.searchParams.append("email", localStorage.getItem("email")!);

        return fetch(url, {
            method: "POST",
        })
            .then(guardResOk)
            .then((res) => res.json())
            .then((data) => {
                updateStorage("access_token", data.access_token);
                updateStorage("refresh_token", data.refresh_token);
                tokens["access_token"] = data.access_token
                tokens["refresh_token"] = data.refresh_token

                return {
                    access_token: data.access_token,
                    refresh_token: data.refresh_token,
                };
            })
            .catch(() => {
                tokens["previous_access_token"] = ""
                return null
            })
    })
};

export const logout = async () => {
    let url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/logout`);
    let accessToken = localStorage.getItem("access_token")!;
    const email = localStorage.getItem("email")!;
    url.searchParams.append("accessToken", accessToken);
    url.searchParams.append("email", email);

    const response = await fetch(url, { method: "POST" });
    if (response.status == 401) {
        console.log("401")
        const refreshTokenResponse = await refreshTokens(accessToken);
        if (refreshTokenResponse === null){
            localStorage.clear();
            window.dispatchEvent(new Event("storage")); 
            return
        }
        url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/logout`);
        accessToken = refreshTokenResponse!["access_token"];
        url.searchParams.append("accessToken", accessToken);
        url.searchParams.append("email", email);
        await fetch(url, { method: "POST" });
        localStorage.clear();
        window.dispatchEvent(new Event("storage"));
    } else {
        localStorage.clear();
        window.dispatchEvent(new Event("storage"));
    }
};

export const deleteAccount = async () => {
    let url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/account`);
    let accessToken = localStorage.getItem("access_token")!;
    const email = localStorage.getItem("email")!;
    url.searchParams.append("accessToken", accessToken);
    url.searchParams.append("email", email);

    const response = await fetch(url, { method: "DELETE" });
    if (response.status == 401) {
        const refreshTokenResponse = await refreshTokens(accessToken);
        if (refreshTokenResponse === null){
            localStorage.clear();
            window.dispatchEvent(new Event("storage")); 
            return
        }
        url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/account`);
        accessToken = refreshTokenResponse!["access_token"];
        url.searchParams.append("accessToken", accessToken);
        url.searchParams.append("email", email);
        await fetch(url, { method: "DELETE" });
        localStorage.clear();
        window.dispatchEvent(new Event("storage"));
    } else {
        localStorage.clear();
        window.dispatchEvent(new Event("storage"));
    }
};

export const updateStorage = (key: string, value: string) => {
    window.localStorage.setItem(key, value);
    window.dispatchEvent(new Event("storage"));
};
