"use client";

import React, { PropsWithChildren, useState } from "react";
import contentMovedByDrawer from "@/styles/contentMovedByDrawer";
import {
    AppBar,
    Box,
    Button,
    Divider,
    Drawer,
    IconButton,
    List,
    Stack,
    Theme,
    Toolbar,
    Typography,
    useMediaQuery,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import NavigationListItem from "./NavigationListItem";

interface Props extends PropsWithChildren {
    pageTitle?: string;
    subpageTitle: string;
    center?: boolean;
}

export const DrawerLayout: React.FC<Props> = ({
    children,
    pageTitle = "GreenMind",
    subpageTitle,
    center = false,
}) => {
    const isDesktop = useMediaQuery((t: Theme) => t.breakpoints.up("md"));
    const [isDrawerOpen, setDrawerOpen] = useState<boolean>(isDesktop);

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
                    {/* {loggedIn ? <UserInfo /> : SignIn} */}

                    <Button variant="contained" color="secondary" onClick={() => /*TODO */ {}}>
                        Zaloguj
                    </Button>
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
                    <NavigationListItem href="account">Konto</NavigationListItem>
                    <NavigationListItem href="plantation">Hodowla</NavigationListItem>
                    <NavigationListItem href="sensors">Sensory</NavigationListItem>
                    <NavigationListItem href="predictions">Prognoza</NavigationListItem>
                    <NavigationListItem href="statistics">Statystyki</NavigationListItem>
                </List>
            </Drawer>
            <Box component="main" sx={[{ p: 2 }, contentMovedByDrawer(isDrawerOpen && isDesktop)]}>
                <Stack alignItems={center ? "center" : "start"} gap={3}>
                    <Stack direction="row" gap={2} sx={{ width: "100%", maxWidth: 800, pb: 2 }}>
                        <Typography variant="h5" component="h2">
                            {subpageTitle}
                        </Typography>
                    </Stack>
                </Stack>
                {children}
            </Box>
        </>
    );
};
