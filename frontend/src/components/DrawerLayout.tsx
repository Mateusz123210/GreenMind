"use client";

import React, { PropsWithChildren, useState } from "react";
import contentMovedByDrawer from "@/styles/contentMovedByDrawer";
import {
    AppBar,
    Box,
    Divider,
    Drawer,
    IconButton,
    List,
    Theme,
    Toolbar,
    Typography,
    useMediaQuery,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import NavigationListItem from "./NavigationListItem";
import AutoGraphIcon from "@mui/icons-material/AutoGraph";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
// import SensorsIcon from "@mui/icons-material/Sensors";
// import YardIcon from '@mui/icons-material/Yard';
import GrassIcon from "@mui/icons-material/Grass";
import FenceIcon from "@mui/icons-material/Fence";
import { LoginButton } from "./LoginButton";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { UserInfo } from "./UserInfo";

interface Props extends PropsWithChildren {
    pageTitle?: string;
    subpageTitle: string;
    center?: boolean;
}

export const DrawerLayout: React.FC<Props> = ({ children, pageTitle = "GreenMind" }) => {
    const isDesktop = useMediaQuery((t: Theme) => t.breakpoints.up("md"));
    const [isDrawerOpen, setDrawerOpen] = useState<boolean>(isDesktop);
    const email = useLocalStorage("email");
    const loggedIn = Boolean(email);

    return (
        <>
            <AppBar position="sticky">
                <Toolbar
                    sx={[
                        { display: "flex", justifyContent: "space-between" },
                        contentMovedByDrawer(isDrawerOpen && isDesktop),
                    ]}
                >
                    <IconButton
                        aria-label="Open menu"
                        color="inherit"
                        hidden={isDrawerOpen}
                        sx={{ visibility: isDrawerOpen ? "hidden" : "visible" }}
                        onClick={() => setDrawerOpen(true)}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h4" component="h1">
                        {pageTitle}
                    </Typography>
                    {loggedIn ? <UserInfo email={email!}/> : <LoginButton />}
                </Toolbar>
            </AppBar>
            <Drawer
                open={isDrawerOpen}
                variant={isDesktop ? "persistent" : "temporary"}
                anchor="left"
                onClose={() => setDrawerOpen(false)}
                PaperProps={{ sx: (t) => ({ width: t.dimensions["drawerWidth"] }) }}
            >
                <Toolbar sx={{ display: "flex", justifyContent: "end" }}>
                    <IconButton aria-label="Close menu" onClick={() => setDrawerOpen(false)}>
                        <ChevronLeftIcon />
                    </IconButton>
                </Toolbar>
                <Divider />
                <List disablePadding>
                    <NavigationListItem href="plants" icon={<GrassIcon />}>
                        Rośliny
                    </NavigationListItem>
                    <Divider variant="middle" />
                    <NavigationListItem href="plantation" icon={<FenceIcon />}>
                        Hodowla
                    </NavigationListItem>
                    <Divider variant="middle" />
                    {/* <NavigationListItem href="sensors" icon={<SensorsIcon />}>
                        Sensory
                    </NavigationListItem>
                    <Divider variant="middle" /> */}
                    <NavigationListItem href="predictions" icon={<AutoAwesomeIcon />}>
                        Prognozy
                    </NavigationListItem>
                    <Divider variant="middle" />
                    <NavigationListItem href="statistics" icon={<AutoGraphIcon />}>
                        Statystyki
                    </NavigationListItem>
                </List>
            </Drawer>
            <Box component="main" sx={[{ p: 2 }, contentMovedByDrawer(isDrawerOpen && isDesktop)]}>
                {children}
            </Box>
        </>
    );
};
