import Form from "../components/Form"

export default function Login() {
    return <Form route="/api/users/token/" method="login" />
}