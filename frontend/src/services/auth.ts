import { enqueueSnackbar } from "notistack";
import { fetchBackend, headersJsonContentType } from "./backend";

export interface User {
    email: string;
    accessToken: string;
    refreshToken: string;
}

export const guardResOk = (res: Response) => {
    if (res.ok) {
        return Promise.resolve(res);
    } else {
        enqueueSnackbar(String(res.body), { variant: "error" });
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

export const refreshTokens = () => {
    const url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/refresh-token`);
    url.searchParams.append("refresh_token", localStorage.getItem("refresh_token")!);
    url.searchParams.append("email", localStorage.getItem("email")!);
    return fetch(url, {
        method: "POST",
    })
        .then(guardResOk)
        .then((res) => res.json())
        .then((data) => {
            updateStorage("email", data.email);
            updateStorage("access_token", data.access_token);
            updateStorage("refresh_token", data.refresh_token);
        });
};

export const logout = () => {
    var url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/logout`);
    const accessToken = localStorage.getItem("access_token")!
    const email = localStorage.getItem("email")!
    url.searchParams.append("accessToken", accessToken);
    url.searchParams.append("email", email);

    fetch(url , { method: "POST" })

    localStorage.clear();
    window.dispatchEvent(new Event("storage"));
};

export const updateStorage = (key: string, value: string) => {
    window.localStorage.setItem(key, value);
    window.dispatchEvent(new Event("storage"));
};
