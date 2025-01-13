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
        // TODO notify
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
    return fetch("api/register", {
        method: "POST",
        headers: headersJsonContentType,
        body: JSON.stringify({
            email,
            password,
        }),
    }).then(guardResOk);
};

export const login = (email: string, password: string) => {
    return fetch("/api/login", {
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
            localStorage.setItem("email", data.email);
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
        });
};

export const refreshTokens = () => {
    const url = new URL("/api/refresh-token");
    url.searchParams.append("refresh_token", localStorage.getItem("refresh_token")!);
    url.searchParams.append("email", localStorage.getItem("email")!);
    return fetch(url, {
        method: "POST",
    })
        .then(guardResOk)
        .then((res) => res.json())
        .then();
};

export const logout = () => {
    fetchBackend("/api/logout", { method: "POST" });
    localStorage.clear();
};
