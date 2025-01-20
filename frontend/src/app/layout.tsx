"use client";

// import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { CssBaseline, ThemeProvider } from "@mui/material";
import theme from "@/styles/theme";
import { DrawerLayout } from "@/components/DrawerLayout";
import { SnackbarProvider } from "notistack";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import "dayjs/locale/pl";

const geistSans = localFont({
    src: "./fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});
const geistMono = localFont({
    src: "./fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

// export const metadata: Metadata = {
//     title: "GreenMind",
//     description: "Manage your plantation with the power of AI",
// };

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={`${geistSans.variable} ${geistMono.variable}`}>
                <ThemeProvider theme={theme}>
                    <LocalizationProvider adapterLocale="pl" dateAdapter={AdapterDayjs}>
                        <CssBaseline />
                        <SnackbarProvider />
                        <DrawerLayout subpageTitle="Dashboard">{children}</DrawerLayout>
                    </LocalizationProvider>
                </ThemeProvider>
            </body>
        </html>
    );
}
