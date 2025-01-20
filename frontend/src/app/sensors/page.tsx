"use client";

import { fetchBackend } from "@/services/backend";
import { useEffect } from "react";

const plantation = "1735683658.5245671485665a807c7-5986-4338-920e-7eba0cfd9528";
export default function Page() {
    useEffect(() => {
        fetchBackend("/api/water", undefined, { plantationUUID: plantation })
            .then((res) => res.text())
            .then(console.log);
    });
    return <>sensor</>;
}
