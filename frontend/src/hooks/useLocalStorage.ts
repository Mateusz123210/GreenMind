"use client";
import { useEffect, useState } from "react";

export const useLocalStorage = (key: string) => {
    const [value, setValue] = useState<string | null>(
        window ? window.localStorage.getItem(key) : null
    );
    useEffect(() => {
        const listener = (ev: StorageEvent) => {
            if (ev.key === key) {
                setValue(ev.newValue);
            }
        };
        window.addEventListener("storage", listener);
        return () => {
            window.removeEventListener("storage", listener);
        };
    });
    return value;
};
