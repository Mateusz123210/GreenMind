"use client";
import { useEffect, useState } from "react";

export const useLocalStorage = (key: string) => {
    const [value, setValue] = useState<string | null>(null);

    useEffect(() => {
        setValue(window.localStorage.getItem(key));
    }, [key])

    useEffect(() => {
        console.log("setting up the storage listener")
        const listener = (ev: StorageEvent) => {
            console.log(ev);
            console.log(key);
            setValue(window.localStorage.getItem(key));
        };
        window.addEventListener("storage", listener);
        return () => {
            window.removeEventListener("storage", listener);
        };
    }, [key]);
    return value;
};
