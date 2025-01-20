import Image from "next/image";
import logo from "@/../assets/logo.webp";

export default function Home() {
    return (
        <>
            <Image
                src={logo}
                style={{ margin: "-16px", width: "calc(100% + 32px)", height: "100%" }}
                alt="ai generated image of a logo with leaves"
            />
        </>
    );
}
