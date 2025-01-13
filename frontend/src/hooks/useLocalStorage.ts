"use client";
import { useEffect, useState } from "react";

export const useLocalStorage = (key: string) => {
    const [value, setValue] = useState<string | null>(null);

    useEffect(() => {
        setValue(window.localStorage.getItem(key));
    }, [key])

    useEffect(() => {
        const listener = (ev: StorageEvent) => {
            console.log(ev);
            if (ev.key === key) {
                setValue(ev.newValue);
            }
        };
        window.addEventListener("storage", listener);
        return () => {
            window.removeEventListener("storage", listener);
        };
    }, [key]);
    return value;
};
