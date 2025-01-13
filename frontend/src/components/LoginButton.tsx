"use client";
import { Button, Dialog, DialogContent, DialogTitle, Tab, Tabs } from "@mui/material";
import { useState } from "react";
import { LoginForm } from "./LoginForm";
import { RegisterForm } from "./RegisterForm";

export const LoginButton: React.FC = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [tabIndex, setTabIndex] = useState<0 | 1>(0);

    const content = {
        0: <LoginForm afterSubmit={() => setIsOpen(false)} />,
        1: <RegisterForm afterSubmit={() => setIsOpen(false)} />,
    };
    return (
        <>
            <Button variant="contained" color="secondary" onClick={() => setIsOpen(true)}>
                Zaloguj
            </Button>
            <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
                <DialogTitle>
                    <Tabs value={tabIndex} onChange={(_, newVal) => setTabIndex(newVal)}>
                        <Tab label="Zaloguj" />
                        <Tab label="Zarejestruj" />
                    </Tabs>
                </DialogTitle>
                <DialogContent>{content[tabIndex]}</DialogContent>
            </Dialog>
        </>
    );
};
