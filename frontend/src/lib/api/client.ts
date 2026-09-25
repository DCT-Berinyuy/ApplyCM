import { API_BASE_URL } from "$lib/config";

const TOKEN_KEY = "access_token";

export class ApiError extends Error {
	constructor(
		public readonly status: number,
		message: string,
	) {
		super(message);
		this.name = "ApiError";
	}
}

interface ValidationIssue {
	loc?: (string | number)[];
	msg?: string;
}

function describeError(status: number, body: unknown): string {
	const detail = (body as { detail?: unknown } | null)?.detail;
	if (typeof detail === "string") return detail;
	if (Array.isArray(detail)) {
		return detail
			.map((issue: ValidationIssue) => {
				const field = issue.loc?.filter((part) => part !== "body").join(".");
				return field ? `${field}: ${issue.msg}` : issue.msg;
			})
			.join("; ");
	}
	return `Request failed (${status})`;
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
	const headers = new Headers(init.headers);
	headers.set("Accept", "application/json");
	if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
	const token = localStorage.getItem(TOKEN_KEY);
	if (token) headers.set("Authorization", `Bearer ${token}`);

	let res: Response;
	try {
		res = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });
	} catch {
		throw new ApiError(0, "Cannot reach the server. Check your connection and try again.");
	}

	if (res.status === 401) {
		localStorage.removeItem(TOKEN_KEY);
		window.location.href = "/login";
		throw new ApiError(401, "Your session has expired. Please log in again.");
	}

	const body = res.status === 204 ? null : await res.json().catch(() => null);
	if (!res.ok) throw new ApiError(res.status, describeError(res.status, body));
	return body as T;
}
